# Import third party modules
import pyotp


def generate_totp_code():
    # Generate secret key in base32 format
    secret_key = pyotp.random_base32()
    # Specify the time step (in seconds)
    time_step = 60
    totp = pyotp.TOTP(secret_key, interval=time_step)
    return totp.now()

