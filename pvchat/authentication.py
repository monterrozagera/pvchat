from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


class Authentication():
    """
        Encryption, decryption and authentication with RSA
    """

    def __init__(self):
        pass

    def keyGenerator(self):
        # Generates private and public keys
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        public_key = private_key.public_key()

        # Send to serialization
        new_private_key, new_public_key = self.keySerialization(private_key, public_key)
        return new_private_key, new_public_key


    def keySerialization(self, private_key, public_key):

        pem = private_key.private_bytes(encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption())

        pub = public_key.public_bytes(encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo)

        return pem, pub