from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import utils


class Authentication():
    """
        Encryption, decryption and authentication with RSA
    """

    def __init__(self):
        pass

    def keyLoader(self, key):
        with open(key, "rb") as key_file:
            private_key = serialization.load_pem_private_key(key_file.read(),
            password=None,
            )
        
        return private_key
        

    def privateKeyGenerator(self):
        # Generates private and public keys
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )

        public_key = self.publicKeyGenerator(private_key)

        # Send to serialization
        new_private_key, new_public_key = self.keySerialization(private_key, public_key)

        # export keys
        self.exportKeys(new_private_key, 'private')
        self.exportKeys(new_public_key, 'public')
        return new_private_key, public_key

    
    def publicKeyGenerator(self, private_key):
        public_key = private_key.public_key()
        return public_key

    def keySerialization(self, private_key, public_key):

        pem = private_key.private_bytes(encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption())

        pub = public_key.public_bytes(encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo)

        return pem, pub

    def exportKeys(self, key, ktype):
        key_contents = key.decode()
        with open(ktype + ".pem", "w") as file1:
            # Writing data to a file
            file1.write(key_contents)

    def encryptMessage(self, message):
        pass

    def decryptMessage(self, encrypted_message):
        pass

    def authenticateKey(self):
        pass