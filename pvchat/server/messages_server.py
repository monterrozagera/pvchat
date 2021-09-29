import socket
import threading
import server_authentication

class messageServer():
    """
        Implements communications between clients.
    """

    def __init__(self, host, port, key):
        self.host = host
        self.port = port
        self.key = key
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        self.auth = server_authentication.Authentication()

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
        authenticated = False
        while True:
            try:
                # recieve messages from clients
                data = client_socket.recv(size)
                print(data.decode())
                # close communication if exit code is received
                if not authenticated:
                    if self.authenticateClient(data):
                        print("Client: {} successfully authenticated!".format(address[0]))
                        client_socket.sendall(bytes('[PASS]', 'utf-8'))
                        authenticated = True
                    else:
                        print("ERROR AUTHENTICATING NEW CLIENT")
                elif 'exit' in data.decode():
                    print("{}:{} is exiting the room".format(address[0], address[1]))
                    client_socket.close()
                    break
                else:
                    # print message in server console
                    formatted_message = "{} says> {}".format(str(address[0]), data.decode())
                    print(formatted_message)
                    self.messageHandler(data.decode())

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

    def authenticateClient(self, request):
        encrypted_request = request
        decrypted_request = self.auth.decryptMessage(self.key, encrypted_request)

        print(decrypted_request)

        if str(decrypted_request) == "b'[SERVER-AUTH-REQUEST]'" or "[SERVER-AUTH-REQUEST]":
            print('ready')
            return True
        else: 
            print("not ready")
            return False

    def exit(self):
        self.server.close()

# stores current clients connected to server
active_users = []