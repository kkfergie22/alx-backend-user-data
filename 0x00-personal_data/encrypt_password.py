#!/usr/bin/env python3

import bcrypt


def hash_password(password: str) -> bytes:
    """Hash password"""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password


def is_valid(hashed_password, password):
    """Check if password is valid"""
    return bcrypt.checkpw(password.encode(), hashed_password)