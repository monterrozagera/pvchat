# TCP Client for PvChat
# Starts connecting to a server on localhost and port 9999 by default
# will accept input to send and receive messages upon execution
import authentication
import client_connect
import sys
import time
import argparse

logo = """██████╗ ██╗   ██╗ ██████╗██╗  ██╗ █████╗ ████████╗
██╔══██╗██║   ██║██╔════╝██║  ██║██╔══██╗╚══██╔══╝
██████╔╝██║   ██║██║     ███████║███████║   ██║   
██╔═══╝ ╚██╗ ██╔╝██║     ██╔══██║██╔══██║   ██║   
██║      ╚████╔╝ ╚██████╗██║  ██║██║  ██║   ██║   
╚═╝       ╚═══╝   ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝  """


HOST, PORT = '192.168.1.110', 9999

if __name__ == '__main__':
    # Start Command Line Parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--key', type=str, help='Private Fernet key.')
    parser.add_argument('--user', type=str, help='Username to use.')
    args = parser.parse_args()

    print(logo)
    
    # Starts auth service
    auth = authentication.Authentication()

    # Checks if key was provided
    if args.key:
        print("[*] Loading key..")
        private_key = auth.loadKey(args.key)
        time.sleep(1)
        print("[!] OK!")
        print(private_key)
    else:
        print("[!] No key was provided.")

    if args.user:
        user_name = args.user
    else:
        user_name = 'anonymous'

    print("\n[!] Logged in as: {}\n".format(user_name))

    try:
        print("[!] Connecting to {}:{}".format(HOST, PORT))
        connected = client_connect.Connection(HOST, PORT, user_name, private_key)
        connected.run()
    except KeyboardInterrupt:
        print("Logged out.")
        time.sleep(1)
        print("Exiting..")
        time.sleep(2)
        sys.exit()