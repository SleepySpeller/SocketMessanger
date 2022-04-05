from email import message
import socket
import threading

nickname = input("Choose a nickname: ")
password = input("Password: ")

connected = False

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 45398))

def recive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            
            if message == 'NICK':
                print(f"[DEBUG]: The server is requesting the username, sending {nickname}")
                client.send(nickname.encode('ascii'))
            elif message == 'PASS':
                print(f"[DEBUG]: The server is requesting the password of the server, sending {password}")
                client.send(password.encode('ascii'))
            elif message == 'ERR_PASS_INC':
                print(f"Incorrect password! Error code {message}")
                break
            elif message == 'ADMIN_PASS':
                print(f"[DEBUG]: The server is requesting the password of the useraccount")
                adminPassword = input(f"The server has requested to enter the password of your account ({nickname}): ")
                client.send(adminPassword.encode('ascii'))
                print(f"[DEBUG]: Password {adminPassword} has been sent")
            elif message == 'ERR_ADMIN_INC':
                print(f"User account password is incorrect, disconnecting... ")
                client.close()
                print("Disconnected. Error code: ERR_ADMIN_INC")
            elif message == 'Connected to the server!':
                write_thread = threading.Thread(target=write)
                write_thread.start()
            else:
                print(message)
        except Exception as e:
            print("An error occurred! Err: ", e)
            client.close()
            break

def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('ascii'))
recive_thread = threading.Thread(target=recive)
recive_thread.start()



