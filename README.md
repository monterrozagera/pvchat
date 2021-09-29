<img width="563" alt="Screen Shot 2021-09-25 at 8 16 37 PM" src="https://user-images.githubusercontent.com/91101951/134792133-98802e96-f519-4d1c-8935-d884c124b6d2.png">

End-to-end encrypted chat server and client developed on python. **Still on development.**

What works right now?
* Key Loading/Generation
* Client connection to server
* Server message forwarding
* Fernet Encryption/Decryption between clients
* Usernames with color

Usage:

First run server:
```
python3 PvChat.py --key *your_key*
```

Then client:
```
python3 PvChatClient.py --key *your_key* --user *your_username*
```

Client will first authenticate with server, start message listener and input will accept messages to send.
