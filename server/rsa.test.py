from utils import Rsa

# Example usage
public_key = open('server.public.pem', 'rb').read()
private_key = open('server.private.pem', 'rb').read()

rsa_instance = Rsa(publicKey=public_key, privateKey=private_key)

# Encrypt data with the public key and get the result in hexadecimal format
encrypted_data_hex = rsa_instance.encrypt(b'This is a secret message')
print(encrypted_data_hex)

# Decrypt data with the private key using the hexadecimal input
decrypted_data = rsa_instance.decrypt(encrypted_data_hex)
print(decrypted_data)

# Sign data with the private key
signature_hex = rsa_instance.sign(b'This is a signed message')
print("Signature:", signature_hex)

# Verify the signature with the public key
verification_result = rsa_instance.verify(b'This is a signed message', signature_hex)
print("Signature Verification Result:", verification_result)
