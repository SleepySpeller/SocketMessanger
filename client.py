import socket
import threading

nickname = input("Choose a nickname: ")
password = input("Password: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 45399))

def recive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            elif message == 'PASS':
                client.send(password.encode('ascii'))
            elif message == 'ERR_PASS_INC':
                print(f"Incorrect password! Error code {message}")
                break
            elif message == 'ADMIN_PASS':
                adminPassword = input(f"The server has requested to enter the password of your account ({nickname}): ")
                client.send(adminPassword.encode('ascii'))
            elif message == 'ERR_ADMIN_INC':
                print(f"User account password is incorrect, disconnecting... ")
                client.close()
                print("Disconnected. Error code: ERR_ADMIN_INC")
            else:
                print(message)
        except:
            print("An error occurred!")
            client.close()
            break

def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('ascii'))
recive_thread = threading.Thread(target=recive)
recive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()