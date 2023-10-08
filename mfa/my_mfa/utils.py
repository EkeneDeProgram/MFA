# Import python standard modules
import secrets
import string
import base64

# Import third party modules
from cryptography.fernet import Fernet


# Generate a 16 character secret key in base32 format for Time-Based One-Time Passwords (TOTP)
def generate_key(length=16):
    # Generate random bytes
    random_bytes = secrets.token_bytes(length)
    # Encode the random bytes in base32
    secret_key = base64.b32encode(random_bytes).decode('utf-8')
    return secret_key


# Generate encryption key
def generate_encryption_key():
    key = Fernet.generate_key()
    return key


# Encrypt totp_secret_key
def encrypt_secret(totp_key, encryption_key):
    # Initialize the Fernet symmetric encryption object with the encryption key
    cipher_suite = Fernet(encryption_key)
    # Convert the TOTP secret key to bytes
    totp_key_bytes = totp_key.encode('utf-8')
    # Encrypt the TOTP secret key
    encrypted_secret = cipher_suite.encrypt(totp_key_bytes)
    return encrypted_secret


# Decypt totp_secret_key
def decrypt_totp_secret_key(encrypted_totp_key, encryption_key):
    cipher_suite = Fernet(encryption_key)
    # Decrypt totp_secret_key
    decrypted_totp_secret_key = cipher_suite.decrypt(encrypted_totp_key)
    # Convert the decrypted data to a UTF-8 encoded string
    decrypted_totp_key_str = decrypted_totp_secret_key.decode('utf-8')
    return decrypted_totp_key_str


