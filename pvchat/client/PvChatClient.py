# TCP Client for PvChat
# Starts connecting to a server on localhost and port 9999 by default
# will accept input to send and receive messages upon execution
import authentication
import client_connect
import sys
import time
import argparse


HOST, PORT = 'localhost', 9999

if __name__ == '__main__':
    # Start Command Line Parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--key', type=str, help='Private Fernet key.')
    args = parser.parse_args()
    
    # Starts auth service
    auth = authentication.Authentication()

    # Checks if key was provided
    if args.key:
        print("Loading key..")
        private_key = auth.loadKey(args.key)
        time.sleep(1)
        print("OK!")
        print(private_key)
    else:
        print("No key was provided.")

    try:
        print("Connecting to {}:{}".format(HOST, PORT))
        connected = client_connect.Connection(HOST, PORT, private_key)
        connected.run()
    except KeyboardInterrupt:
        print("Logged out.")
        time.sleep(1)
        print("Exiting..")
        time.sleep(2)
        sys.exit()