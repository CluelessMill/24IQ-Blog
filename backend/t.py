from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import hashlib

def encrypt_message(message, key):
    # Create a cipher object using AES in ECB mode
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()
    
    # Pad the message to be a multiple of 16 bytes (AES block size)
    padder = padding.PKCS7(128).padder()
    padded_message = padder.update(message.encode()) + padder.finalize()
    
    # Encrypt the padded message
    ciphertext = encryptor.update(padded_message) + encryptor.finalize()
    
    return ciphertext

def decrypt_message(encrypted_message, key):
    # Create a cipher object using AES in ECB mode
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_message = decryptor.update(encrypted_message) + decryptor.finalize()
    # Unpad the decrypted message
    unpadder = padding.PKCS7(128).unpadder()
    unpadded_message = unpadder.update(decrypted_message) + unpadder.finalize()
    return unpadded_message.decode()

# Example usage:
key = hashlib.sha256(b'my_secret_key').digest()[:16]  # AES requires a 16-byte key
message = "Hello, world!"

encrypted_message = encrypt_message(message, key)
print("Encrypted:", encrypted_message)

decrypted_message = decrypt_message(encrypted_message, key)
print("Decrypted:", decrypted_message)
