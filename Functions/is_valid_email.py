import re


def is_valid_email(email):
    pattern = r'^\s*[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\s*$'
    return re.match(pattern, email) is not None
