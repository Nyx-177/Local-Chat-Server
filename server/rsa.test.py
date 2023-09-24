from utils import Rsa

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
