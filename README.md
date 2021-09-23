# pvchat
Private chat server and client developed on python. **Still on development.**

What works right now?
* Key Loading/Generation
* Client connection to server
* Server message forwarding
* Encryption/Decryption between clients
* Basic functionalities

Usage:

First run server:
```
python3 PvChat.py --key *your_key*
```

Then client:
```
python3 PvChatClient.py --key *your_key*
```

Client will first authenticate with server, start message listener and input will accept messages to send.
