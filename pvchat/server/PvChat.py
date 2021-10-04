# TCP Server for PvChat
# Starts server in localhost and port 9999 by default
import server_authentication
import messages_server
import argparse
import time
import sys

logo = """ ██▓███   ██▒   █▓ ▄████▄   ██░ ██  ▄▄▄     ▄▄▄█████▓
▓██░  ██▒▓██░   █▒▒██▀ ▀█  ▓██░ ██▒▒████▄   ▓  ██▒ ▓▒
▓██░ ██▓▒ ▓██  █▒░▒▓█    ▄ ▒██▀▀██░▒██  ▀█▄ ▒ ▓██░ ▒░
▒██▄█▓▒ ▒  ▒██ █░░▒▓▓▄ ▄██▒░▓█ ░██ ░██▄▄▄▄██░ ▓██▓ ░ 
▒██▒ ░  ░   ▒▀█░  ▒ ▓███▀ ░░▓█▒░██▓ ▓█   ▓██▒ ▒██▒ ░ 
▒▓▒░ ░  ░   ░ ▐░  ░ ░▒ ▒  ░ ▒ ░░▒░▒ ▒▒   ▓▒█░ ▒ ░░   
░▒ ░        ░ ░░    ░  ▒    ▒ ░▒░ ░  ▒   ▒▒ ░   ░    
░░            ░░  ░         ░  ░░ ░  ░   ▒    ░      
               ░  ░ ░       ░  ░  ░      ░  ░        
              ░   ░                                 """

# IP and PORT
HOST, PORT = 'localhost', 9999


if __name__ == '__main__':
    # Start Command Line Parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--key', type=str, help='Private Fernet key to start server.')
    args = parser.parse_args()
    print()
    print(logo)
    print()

    print("[!] Initializing server on {}:{}".format(HOST, PORT))

    # start auth service
    auth = server_authentication.Authentication()

    if args.key:
        print("[*] Loading key..")
        # if key was provided, will load to private_key var
        private_key = auth.loadKey(args.key)
        time.sleep(2)
        print("[!] OK")
    else:
        print("[!] No key provided.")
        print()
        generate_key = input("[*] Generate key? y/n\n")
        if generate_key == 'y':
            # generate key
            new_key = auth.generateKey()
            print()
            print("[!] New key generated! Now load it with the --key arg.")
            sys.exit(0)
        else:
            sys.exit(0)

    try:
        # start server
        startServer = messages_server.messageServer(HOST, PORT, private_key)
        startServer.startClientListener()
    except KeyboardInterrupt:
        # closes connection and exits
        startServer.exit()
        print("\n\nClosing connection...\n")
        print("Bye!")