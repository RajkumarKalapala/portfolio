"""
core/password_gen.py
Generate cryptographically secure OTP / passwords.
"""

import secrets
import string


def generate_password(length: int = 12, use_symbols: bool = True) -> str:
    """
    Generate a secure random password.
    - Includes uppercase, lowercase, digits, and optionally symbols.
    """
    alphabet = string.ascii_letters + string.digits
    if use_symbols:
        alphabet += "!@#$%^&*"

    # Guarantee at least one of each required type
    pwd = [
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.digits),
    ]
    if use_symbols:
        pwd.append(secrets.choice("!@#$%^&*"))

    # Fill remaining length
    pwd += [secrets.choice(alphabet) for _ in range(length - len(pwd))]

    # Shuffle to avoid predictable positions
    secrets.SystemRandom().shuffle(pwd)
    return "".join(pwd)


def generate_otp(digits: int = 6) -> str:
    """Generate a numeric OTP."""
    return "".join([str(secrets.randbelow(10)) for _ in range(digits)])
