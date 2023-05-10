#!/usr/bin/env python3

"""Authentication Module"""

import bcrypt


def _hashed_password(password: str) -> bytes:
    """Returns a salted, hashed password, which is a byte string."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
