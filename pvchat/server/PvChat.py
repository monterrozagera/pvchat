# TCP Server for PvChat
# Starts server in localhost and port 9999 by default
import messages_server
import authentication
import file_handler
import argparse
import sys

# IP and PORT
HOST, PORT = 'localhost', 9999


if __name__ == '__main__':
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


    print("Initializing server on {}:{}".format(HOST, PORT))

    try:
        startServer = messages_server.messageServer(HOST, PORT)
        startServer.startClientListener()
    except KeyboardInterrupt:
        # closes connection and exits
        startServer.exit()
        print("\n\nClosing connection...\n")
        print("Bye!")