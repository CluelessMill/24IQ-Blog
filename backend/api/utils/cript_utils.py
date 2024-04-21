from ast import literal_eval

from bcrypt import checkpw, gensalt, hashpw
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from django.conf import settings

CYPHER_KEY = settings.CYPHER_KEY


def encrypt(data) -> bytes:
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(data.encode())
    hashed_message = digest.finalize()
    cipher = Cipher(algorithms.AES(CYPHER_KEY), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_message = encryptor.update(hashed_message) + encryptor.finalize()
    return encrypted_message


def decrypt(data) -> bytes:
    cipher = Cipher(algorithms.AES(CYPHER_KEY), modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_message = decryptor.update(data) + decryptor.finalize()
    return decrypted_message


def hash_password(password) -> bytes:
    salt = gensalt()
    hashed_password = hashpw(password.encode("utf-8"), salt)
    return hashed_password


def check_password(input_password, stored_password) -> bool:
    stored_bytes = literal_eval(stored_password)
    return bool(checkpw(input_password.encode("utf-8"), stored_bytes))
