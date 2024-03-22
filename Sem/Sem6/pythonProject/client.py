import socket
import threading

# Choosing Nickname
nickname = input("Choose your nickname: ")

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

# Listening to Server and Sending Nickname
def receive():
    while True:
        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            # Close Connection When Error
            print("An error occurred!")
            client.close()
            break

def write():
    while True:
        message = input('')
        if message.lower() == 'exit':
            client.send('exit'.encode('ascii'))
            break
        elif message.startswith("@"):
            recipient = message.split()[0][1:]
            private_message = ' '.join(message.split()[1:])
            client.send('@{} {}'.format(recipient, private_message).encode('ascii'))
        else:
            message = '{}: {}'.format(nickname, message)
            client.send(message.encode('ascii'))

# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()