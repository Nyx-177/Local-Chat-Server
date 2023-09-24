from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_PSS
from Crypto.Hash import SHA256
import binascii

class Rsa:
    def __init__(self, publicKey=None, privateKey=None):
        if publicKey:
            self.public_key = RSA.import_key(publicKey)
        else:
            self.public_key = None

        if privateKey:
            self.private_key = RSA.import_key(privateKey)
        else:
            self.private_key = None
        
    def decrypt(self, data):
        if self.private_key:
            cipher = PKCS1_OAEP.new(self.private_key)
            try:
                decrypted_data = cipher.decrypt(data)
                return decrypted_data
            except Exception:
                return False
        else:
            return False

    def encrypt(self, data, withPrivate=False):
        if withPrivate:
            key_to_use = self.private_key
        else:
            key_to_use = self.public_key

        if key_to_use:
            cipher = PKCS1_OAEP.new(key_to_use)
            encrypted_data = cipher.encrypt(data)
            return encrypted_data
        else:
            return False

    def sign(self, data):
        if self.private_key:
            signer = PKCS1_PSS.new(self.private_key)
            h = SHA256.new(data)
            try:
                signature = signer.sign(h)
                signature_hex = binascii.hexlify(signature).decode()
                return signature_hex
            except Exception:
                return False
        else:
            return False

    def verify(self, data, signature_hex):
        if self.public_key:
            verifier = PKCS1_PSS.new(self.public_key)
            h = SHA256.new(data)
            signature = binascii.unhexlify(signature_hex)
            return verifier.verify(h, signature)
        else:
            return False

# Example usage
public_key = open('public.pem', 'rb').read()
private_key = open('private.pem', 'rb').read()

rsa_instance = Rsa(publicKey=public_key, privateKey=private_key)

# Encrypt data with the public key
encrypted_data = rsa_instance.encrypt(b'This is a secret message')
print(encrypted_data)

# Decrypt data with the private key
decrypted_data = rsa_instance.decrypt(encrypted_data)
print(decrypted_data)

# Sign data with the private key
signature_hex = rsa_instance.sign(b'This is a signed message')
print("--- Start Signed Message ---\n{message}\n--- Start Signature ---\n{signature}\n--- End Signature ---".format(message=b'This is a signed message', signature=signature_hex))

print(".")
# Verify the signature with the public key
verification_result = rsa_instance.verify(b'This is a signed message', signature_hex)
print("Signature Verification Result:", verification_result)
