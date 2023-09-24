from utils import log

import rsa  # You can use the 'rsa' library to handle RSA encryption and signing

class Rsa:
    def __init__(self, publicKey=None, privateKey=None):
        self.public_key = publicKey
        self.private_key = privateKey
        
        if not self.private_key and self.public_key:
            # Try to extract the public key from the given private key
            try:
                self.private_key = rsa.PrivateKey.load_pkcs1(self.public_key)
            except Exception:
                self.private_key = None

    def decrypt(self, data):
        try:
            decrypted_data = rsa.decrypt(data, self.private_key)
            return decrypted_data
        except Exception:
            return False

    def encrypt(self, data, withPrivate=False):
        if withPrivate:
            key_to_use = self.private_key
        else:
            key_to_use = self.public_key

        if key_to_use:
            encrypted_data = rsa.encrypt(data, key_to_use)
            return encrypted_data
        else:
            return False

    def sign(self, data):
        if self.private_key:
            signature = rsa.sign(data, self.private_key, 'SHA-256')
            return signature
        else:
            return False


# generate public and private keys with:
# openssl genrsa -out private.pem 2048
# openssl rsa -in private.pem -outform PEM -pubout -out public.pem


# Example usage
public_key = open('public.pem', 'r').read()
private_key = open('private.pem', 'r').read()

rsa_instance = Rsa(publicKey=public_key, privateKey=private_key)

# Encrypt data with the public key
encrypted_data = rsa_instance.encrypt(b'This is a secret message')
print(encrypted_data)

# Decrypt data with the private key
decrypted_data = rsa_instance.decrypt(encrypted_data)
print(decrypted_data)

# Sign data with the private key
signature = rsa_instance.sign(b'This is a signed message')
print(signature)
