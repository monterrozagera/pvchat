class Files():
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