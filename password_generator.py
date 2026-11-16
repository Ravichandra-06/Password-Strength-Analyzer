import secrets
import string

def generate_password(length=16):
    if length < 12:
        raise ValueError("Password length must be at least 12.")

    characters = (
        string.ascii_uppercase +
        string.ascii_lowercase +
        string.digits +
        "!@#$%^&*()-_=+"
    )

    while True:
        password = ''.join(
            secrets.choice(characters)
            for _ in range(length)
        )

        if (
            any(c.isupper() for c in password)
            and any(c.islower() for c in password)
            and any(c.isdigit() for c in password)
            and any(c in "!@#$%^&*()-_=+" for c in password)
        ):
            return password
