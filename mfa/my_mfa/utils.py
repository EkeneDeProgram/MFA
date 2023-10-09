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
    try:
        # Initialize the Fernet symmetric encryption object with the encryption key
        cipher_suite = Fernet(encryption_key)
        encrypted_secret = cipher_suite.encrypt(totp_key.encode())
        return encrypted_secret
    except Exception as e:
        # Handle encryption error
        print("Encryption error:", e)
        return None


# Decypt totp_secret_key
def decrypt_totp_secret_key(encrypted_totp_key, encryption_key):
    try:
        cipher_suite = Fernet(encryption_key)
        # Decrypt totp_secret_key
        decrypted_totp_secret_key = cipher_suite.decrypt(encrypted_totp_key).decode()
        return decrypted_totp_secret_key
    except Exception as e:
        # Handle decryption error
        print("Decryption error:", e)
        return None


x = generate_key()
y = generate_encryption_key()
print(x)
print(y)
z = encrypt_secret(x, y)
print(z)
a = decrypt_totp_secret_key(z, y)
print(a)