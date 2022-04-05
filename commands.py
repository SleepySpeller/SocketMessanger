import socket
import re
import getAllCommands
import importlib
import sys
import pickle

class command:
    def __init__(self, message, client, nicknames, clients, admins):
        self.message = message
        self.client = client
        self.nicknames = nicknames
        self.clients = clients
        self.admins = admins

    def importLibs():
        with open('initalizedCommands', 'rb') as f:
            statusInitalizedLibs = pickle.load(f)
        
        if(statusInitalizedLibs == False):
            try:
                statusInitalizedLibs = False
                with open('initalizedCommands', 'wb') as se:
                    pickle.dump(statusInitalizedLibs, se)

                list = getAllCommands.getListOfFiles("commands")
                sys.path.append('commands\\')

                for i in range(len(list)-1):
                    print(len(list))
                        
                    lib = str(list[i])

                    libLen = len(lib)

                    lib = lib[9:libLen - 3]

                    if("__pycache__" in lib):
                        continue
                    else:
                        print("importing ", lib)
                        importlib.import_module(lib)
            except:
                print("Importing error!")

    def commandInfo(message, client, nicknames):
       client.send("This server has been made by SleepySpeller#0289!".encode('ascii'))

    def kickUser(message, client, nicknames):
        print("Kicking function called!")
        message = message.lower()
        x = re.findall("kick", message)
        print("/kick found in ", x)

    def commandHandler(message, client, nicknames, clients, admins):
            command.importLibs()
            
            print(list)
            print("commandHandler called!")
            try:
                scannedMessage = re.findall("/info", message)
                print(message)
                print(scannedMessage)

                if scannedMessage:
                    print("found /info in message")
                    command.commandInfo(message, client, nicknames)
                else:
                    print("commands not found in the message")
            except Exception as e:
                print("commandHandler error, aka ", e)    



