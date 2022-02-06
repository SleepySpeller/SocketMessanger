from re import I
import threading
import socket

inputPassword = ""
inputPasswordAdmin = ""
success = True

host = "127.0.0.1"
port = 45399
password = "abc"

admins = ["Speller"]
adminPasswords = ["def"]

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))

server.listen()

clients = []
nicknames = []

#send messages for all clients
def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat!'.encode('ascii'))
            nicknames.remove(nickname)
            break

def recive():
    while True:
        try:
            client, address = server.accept()
            print(f"Connected with {str(address)}")

            success = True
            ## Requesting the client to send the username
            print("[DEBUG]: Requesting the nickname (Tag: NICK)")
            client.send('NICK'.encode('ascii'))
            nickname = client.recv(1024).decode('ascii')
            print(f"[DEBUG]: Recived nickname {nickname}")

            ## Requesting the client to send the password for the server
            print(f"[DEBUG]: Requesting the password of the server")
            client.send('PASS'.encode('ascii'))
            inputPassword = client.recv(1024).decode('ascii')
            print(f"[DEBUG]: Recived {inputPassword} as a password from the user")

            ## Checking if the password is correct
            if inputPassword == password:
                print(f"[DEBUG]: Password is correct")
                pass
            else:
                print(f"[DEBUG]: Password is incorrect")
                client.send('ERR_PASS_INC'.encode('ascii'))
                client.close()
                success = False
                break

            for i in range(len(admins)):
                if str(admins[i]) == str(nickname):
                    print(f"[DEBUG]: The user is the Admin, requesting the password of his account")
                    client.send('ADMIN_PASS'.encode('ascii'))
                    inputPasswordAdmin = client.recv(1024).decode('ascii')
                    print(f"[DEBUG]: Recived {inputPasswordAdmin} as a password from the admin account")
                    
                    if inputPasswordAdmin == adminPasswords[i]:
                        print(f"[DEBUG]: Admin password is correct")
                        pass
                    else:
                        client.send('ERR_ADMIN_INC'.encode('ascii'))
                        client.close()
                        success = False
                        print(f"[DEBUG]: Admin password is incorrect")
                        break
            if success == True:
                try:
                    print(f"[DEBUG]: Trying to connect the user to the chat room")
                    nicknames.append(nickname)
                    clients.append(client)

                    print(f"Nickname of the client is {nickname}!")
                    broadcast(f'{nickname} joined the chat!'.encode('ascii'))
                    client.send('Connected to the server!'.encode('ascii'))

                    thread = threading.Thread(target=handle, args=(client, ))
                    thread.start()
                except:
                    print(f"[DEBUG]: Unable to connect the user to the chat room")
                    #client.send('ERR_SOCK_LOG')
                    #client.close
        except:
            print("Error connecting the client!")        


print("Server is listening!")
recive()

if __name__ == "__main__":
    recive()  