# Import python standard modules
import secrets
import string
import base64
import pyotp

# Import third party modules
from cryptography.fernet import Fernet


def sky():
    secret_key = pyotp.random_base32()
    return secret_key

def generate_encryption_key():
    # Generate a random encryption key
    encryption_key = Fernet.generate_key()
    return encryption_key



def encrypt_secret_key(secret_key, encryption_key):
    # Initialize the Fernet cipher with the provided encryption key
    cipher_suite = Fernet(encryption_key)
    # Convert the secret_key (Base32) to bytes
    secret_key_bytes = secret_key.encode('utf-8')
    # Encrypt the secret_key
    encrypted_secret_key = cipher_suite.encrypt(secret_key_bytes)
    return encrypted_secret_key

def decrypt_secret_key(encrypted_secret_key, encryption_key):
    # Initialize the Fernet cipher with the provided encryption key
    cipher_suite = Fernet(encryption_key)
    # Decrypt the encrypted_secret_key
    decrypted_secret_key = cipher_suite.decrypt(encrypted_secret_key)
    
    # Convert the decrypted bytes back to a string (assuming it was originally in UTF-8 encoding)
    secret_key = decrypted_secret_key.decode('utf-8')
    return secret_key


def is_valid_base32_key(key):
    try:
        # Attempt to decode the key from base32
        decoded_key = base64.b32decode(key, casefold=True)

        # Check the length (valid keys are typically 16 or 32 bytes)
        if len(decoded_key) in (16, 32):
            return True
    except Exception:
        pass

    return False   

y = "HQORCRTUVRBMDIWB5GZMISDZA7HVQGA6"
x = is_valid_base32_key(y)
print(x)