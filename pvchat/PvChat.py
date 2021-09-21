# TCP Server for PvChat
# Starts server in localhost and port 9999 by default
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import socket
import threading
import argparse
import sys

def logsHandler():
    # checks if log file exist and creates one
    try:
        logs = open('chat_logs.txt', 'r')
        return logs
    except FileNotFoundError:
        print("\n[!] Logs don't exist. Creating log file..\n")
        logs = open('chat_logs.txt', 'x')
        return logs

def userdatabaseHandler():
    # checks for database
    try:
        database = open('users.txt', 'r')
        return database
    except FileNotFoundError:
        print("[!] Database not found. Creating database..\n")
        database = open('users.txt', 'x')
        return database

def keyLoader(keyLocation):
    try:
        key = open(keyLocation, 'r')
        return key
    except FileNotFoundError:
        print("[!] Error loading key.")


# UNCOMMENT THIS SECTION for database creation
# logs = logsHandler()
# users_file = userdatabaseHandler()

# stores current clients connected to server
active_users = []

class Authentication():
    """
        Encryption, decryption and authentication with RSA
    """

    def __init__(self):
        pass

    def keyGenerator(self):
        # Generates private and public keys
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        public_key = private_key.public_key()

        # Send to serialization
        new_private_key, new_public_key = self.keySerialization(private_key, public_key)
        return new_private_key, new_public_key


    def keySerialization(self, private_key, public_key):

        pem = private_key.private_bytes(encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption())

        pub = public_key.public_bytes(encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo)

        return pem, pub


class messageServer():
    """
        Implements communications between clients.
    """

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(5)

    # appends and prints active clients
    def activeClients(self, client):
        if client not in active_users:
            active_users.append(client)

    # starts listener service
    def startClientListener(self):
        while True:
            client, addr = self.server.accept()
            print(
                "Accepted connection from: {}:{}".format(addr[0], addr[1])
            )
            threading.Thread(target=self.handleClient, args=(client,addr)).start()
            self.activeClients(client)

    # handles and create individual processes for clients
    def handleClient(self, client_socket, address):
        size = 1024
        while True:
            try:
                # recieve messages from clients
                data = client_socket.recv(size)
                # close communication if exit code is received
                if 'exit' in data.decode():
                    print("{}:{} is exiting the room".format(address[0], address[1]))
                    client_socket.close()
                    break
                else:
                    # print message in server console
                    formatted_message = "{} says> {}".format(str(address[0]), data.decode())
                    print(formatted_message)
                    self.messageHandler(formatted_message)

                    # UNCOMMENT FOR LOG MESSAGING
                    # self.logMessage(formatted_message)
                    

            except socket.error:
                client_socket.close()
                return False

    # forwards messages to all clients
    def messageHandler(self, message):
        for c in active_users:
            c.sendall(bytes(message, 'utf-8'))
    
    # unused, registers IP in file
    def registerUser(self, ip_address):
        I_P = ip_address + '\n'
        with open('users.txt', 'a') as f:
            f.write(I_P)

    # logs messages to log file
    def logMessage(self, message):
        log_message = message + '\n'
        with open('chat_logs.txt', 'a') as f:
            f.write(log_message)

     # Checks if client is registered in DB
    def checkUserIP(self, IP):
        client = IP
        with open('users.txt') as f:
            if client in f.read():
                return True
            else:
                print("[!] CONNECTION COMMING FROM NEW IP.\n")
                print("Registering new user..")
                print("Done.")
                self.registerUser(client)
                return True

    def exit(self):
        self.server.close()


# IP and PORT
HOST, PORT = 'localhost', 9999


if __name__ == '__main__':
    # Start Command Line Parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--key', type=str, help='Private RSA key to start server.')
    args = parser.parse_args()
    
    # Starts auth service
    auth = Authentication()

    # Checks if key was provided
    if args.key:
        key = keyLoader(args.key).read()
    else:
        print("No private key was provided.")
        generateKey = input("Generate key? y/n\n> ")
        if generateKey == 'y':
            # Generates new keys
            private_key, public_key = auth.keyGenerator()
            print("This is your new private key: ")
            print(private_key)
            print()
        else:
            sys.exit(1)



    print("Initializing server on {}:{}".format(HOST, PORT))

    try:
        startServer = messageServer(HOST, PORT)
        startServer.startClientListener()
    except KeyboardInterrupt:
        # closes connection and exits
        startServer.exit()
        print("\n\nClosing connection...\n")
        print("Bye!")