import authentication
import threading
import socket
import sys
import re

class Connection(threading.Thread):
    """
        TCP ClientConnection Handler
    """

    def __init__(self, host, port, user_name, key):
        threading.Thread.__init__(self)
        # connection variables
        self.host = host
        self.port = port
        self.user_name = user_name
        self.key = key
        self.client_authenticated = False
        self.auth = authentication.Authentication()
        # connect to socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        self.sock.settimeout(.1)
        self.startListener()
        self.startMessenger()
        
        
    def startMessenger(self):
        t = threading.Thread(target=self.messageSender).start()

    def messageSender(self):
        try:
            alive = True
            loaded = False
            while alive == True:
                if self.client_authenticated:

                    if loaded == False:
                        print('\nFully loaded. Type your message below:')
                        loaded = True

                    messageSend = input()
                    formated_message = "#{}>{}".format(self.user_name, messageSend)
                    encryptedMessage = self.encryptMessage(formated_message)

                    # delete previous row for clean up
                    print("\033[A                             \033[A")
                    if messageSend == 'exit':
                        self.logOut()   
                    self.sock.sendall(encryptedMessage)
        
        except KeyboardInterrupt:
            self.logOut()

    def messageListener(self):
        # receive and print message
        try:
            start = 0
            authenticating = 0
            while True:
                if start < 1:
                    print("Listener [OK]")
                    start += 1

                message = ''

                if self.client_authenticated == False:
                    if authenticating < 1:
                        print("Sending authentication request to server..")
                        request = self.authenticateToServer()
                        self.sock.sendall(request)
                        authenticating += 1

                # listen for messages
                try:
                    message = self.sock.recv(1024)
                except (socket.timeout, OSError) as e:
                    pass

                # if message is received, print message
                if self.client_authenticated == False:
                    if message.decode() == '[PASS]':
                        print()
                        self.client_authenticated = True
                        print('AUTHENTICATED NICE!')
                elif message != '':
                    decrypted_message = self.auth.decryptMessage(self.key, message)
                    user_nameFormat = re.findall("#.*>", decrypted_message.decode())
                    messageFormat = re.sub("#.*>", "", decrypted_message.decode())

                    print("\033[44;33m{}\033[m {}".format(user_nameFormat[0], messageFormat))    
                
        except (socket.timeout, KeyboardInterrupt) as e:
            pass
    
    def startListener(self):
        # start listener thread
        tu = threading.Thread(target=self.messageListener).start()

    def encryptMessage(self, message):
        encrypted_message = self.auth.encryptMessage(self.key, message)
        return encrypted_message

    def authenticateToServer(self):
        request = '[SERVER-AUTH-REQUEST]'
        encrypted_request = self.auth.encryptMessage(self.key, request)
        return encrypted_request

    def logOut(self):
        # tried going around the lock error
        threading.Lock.release()
        self.sock.sendall(bytes('exit', "utf-8"))
        self.sock.shutdown(1)
        self.sock.close()
        sys.exit(0)