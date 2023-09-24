from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

class Rsa:
    def __init__(self, publicKey=None, privateKey=None):
        self.private_key = None
        self.public_key = None

        if publicKey:
            self.public_key = RSA.import_key(publicKey)
        if privateKey:
            self.private_key = RSA.import_key(privateKey)

        if not self.private_key and not self.public_key:
            self.private_key = RSA.generate(2048)
            self.public_key = self.private_key.publickey()

        if not self.private_key and publicKey:
            self.private_key = False
        
        if not self.public_key and privateKey:
            self.public_key = RSA.import_key(privateKey).publickey()

    def decrypt(self, data):
        if self.private_key:
            try:
                cipher = PKCS1_OAEP.new(self.private_key)
                decrypted_data = cipher.decrypt(data)
                return decrypted_data
            except Exception:
                return False
        else:
            return False

    def encrypt(self, data, withPrivate=False):
        if withPrivate and self.private_key:
            cipher = PKCS1_OAEP.new(self.private_key)
        elif self.public_key:
            cipher = PKCS1_OAEP.new(self.public_key)
        else:
            return False

        encrypted_data = cipher.encrypt(data)
        return encrypted_data

    def sign(self, data):
        if self.private_key:
            try:
                h = SHA256.new(data)
                signature = pkcs1_15.new(self.private_key).sign(h)
                return signature
            except Exception:
                return False
        else:
            return False

# Example usage
public_key = open('public.pem', 'rb').read()
private_key = open('private.pem', 'rb').read()

rsa_instance = Rsa(privateKey=private_key)

# Encrypt data with the public key
encrypted_data = rsa_instance.encrypt(b'This is a secret message')
print(encrypted_data)

# Decrypt data with the private key
decrypted_data = rsa_instance.decrypt(encrypted_data)
print(decrypted_data)

# Sign data with the private key
signature = rsa_instance.sign(b'This is a signed message')
print(signature)
