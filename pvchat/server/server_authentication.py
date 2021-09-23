from cryptography.fernet import Fernet


class Authentication():
    """
        Encryption, decryption and authentication with Fernet
    """

    def __init__(self):
        pass

    def loadKey(self, key):
        with open(key, 'r') as imported_key:
            key = imported_key.read()
            return key

    def generateKey(self):
        new_key = Fernet.generate_key()
        return new_key

    def exportKey(self, key):
        with open("new_key.key", "w") as exported_key:
            exported_key.write(str(key)) 

    def encryptMessage(self, key, message):
        k = Fernet(key)
        encrypted = k.encrypt(bytes(message, 'utf-8'))
        return encrypted

    def decryptMessage(self, key, encrypted_message):
        k = Fernet(key)
        decrypted = k.decrypt(encrypted_message)
        return decrypted

    def authenticationRequest(self, key):
        token = '[SERVER-AUTH-REQUEST]'
        request = self.encryptMessage(key, token)
        return request