# Import third party modules
import re


# Validate email format
def is_valid_email(email):
    email_pattern = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')
    return email_pattern.match(email)