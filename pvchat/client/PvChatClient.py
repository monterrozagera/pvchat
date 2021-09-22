# TCP Client for PvChat
# Starts connecting to a server on localhost and port 9999 by default
# will accept input to send and receive messages upon execution
import file_handler
import authentication
import socket
import sys
import threading
import time
import argparse # not yet used

class Authentication():
    """
        RSA Generator and authenticator
    """

    def __init__(self):
        pass

    def loadKey(self):
        pass

    def verifyKey(self):
        pass

    def requestKey(self):
        pass

class Connection(threading.Thread):
    """
        TCP ClientConnection Handler
    """

    def __init__(self, host, port):
        threading.Thread.__init__(self)
        # connection variables
        self.host = host
        self.port = port
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
            while alive == True:
                messageSend = input()

                # delete previous row for clean up
                print("\033[A                             \033[A")
                if messageSend == 'exit':
                    self.logOut()             

                self.sock.sendall(bytes(messageSend, "utf-8"))
        
        except KeyboardInterrupt:
            self.logOut()

    def messageListener(self):
        # receive and print message
        try:
            start = 0
            while True:
                if start < 1:
                    print("Okay listener running..")
                    start += 1

                message = ''

                # listen for messages
                try:
                    message = self.sock.recv(1024)
                except (socket.timeout, OSError) as e:
                    pass

                # if message is received, print message
                if message != '':
                    print(message.decode())          
                
        except (socket.timeout, KeyboardInterrupt) as e:
            pass
    
    def startListener(self):
        # start listener thread
        tu = threading.Thread(target=self.messageListener).start()

    def authenticateToServer(self, public_key):
        pass

    def logOut(self):
        # tried going around the lock error
        threading.Lock.release()
        self.sock.sendall(bytes('exit', "utf-8"))
        self.sock.shutdown(1)
        self.sock.close()
        sys.exit(0)


HOST, PORT = 'localhost', 9999


connected = Connection(HOST, PORT)

if __name__ == '__init__':
    # Start Command Line Parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--key', type=str, help='Private RSA key to start server.')
    args = parser.parse_args()
    
    # Starts auth service
    auth = authentication.Authentication()

    # Checks if key was provided
    if args.key:
        key = file_handler.Files.keyLoader(args.key).read()
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

try:
    connected.run()
except KeyboardInterrupt:
    print("Logged out.")
    time.sleep(1)
    print("Exiting..")
    time.sleep(2)
    sys.exit()