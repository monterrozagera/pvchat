import socket
import threading

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

# stores current clients connected to server
active_users = []