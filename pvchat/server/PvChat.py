# TCP Server for PvChat
# Starts server in localhost and port 9999 by default
import messages_server
import argparse

# IP and PORT
HOST, PORT = 'localhost', 9999


if __name__ == '__main__':
    # Start Command Line Parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--start', type=str, help='Private RSA key to start server.')
    args = parser.parse_args()


    print("Initializing server on {}:{}".format(HOST, PORT))

    try:
        startServer = messages_server.messageServer(HOST, PORT)
        startServer.startClientListener()
    except KeyboardInterrupt:
        # closes connection and exits
        startServer.exit()
        print("\n\nClosing connection...\n")
        print("Bye!")