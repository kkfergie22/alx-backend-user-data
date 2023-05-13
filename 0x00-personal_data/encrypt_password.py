#!/usr/bin/env python3

"""Module for obfuscating personal data fields and encrypting passwords"""

import bcrypt


def hash_password(password: str) -> bytes:
    """Hash password"""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Check if password is valid"""
    return bcrypt.checkpw(password.encode(), hashed_password)
