#!/usr/bin/env python3

"""Authentication Module"""

import bcrypt
from db import DB
import uuid
from user import User
from typing import Union
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Returns a salted, hashed password, which is a byte string."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generate a UUID"""
    return str(uuid.uuid4())


class Auth:
    """"Auth class to interact with the authentication database."""
    def __init__(self) -> None:
        """Constructor"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a user"""
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError(f'User {email} already exists')

    def valid_login(self, email: str, password: str) -> bool:
        """ Check if the login is valid """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        entered_password = password.encode('utf-8')
        hashed_password = user.hashed_password
        return bcrypt.checkpw(entered_password, hashed_password)

    def create_session(self, email: str) -> str:
        """ Create a session ID """
        try:
            user = self._db.find_user_by(email=email)
            if user is None:
                return None
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[str, None]:
        """ Get a user from a session ID """
        if session_id:
            try:
                return self._db.find_user_by(session_id=session_id)
            except NoResultFound:
                return None
        return None

    def destroy_session(self, user_id: int) -> None:
        """ Destroy a session """
        if user_id:
            try:
                self._db.update_user(user_id, session_id=None)
            except NoResultFound:
                return None
        return None

    def get_reset_password_token(self, email: str) -> str:
        """ Get a reset password token """
        try:
            user = self._db.find_user_by(email=email)
            if user is None:
                raise ValueError("User does not exist")
            reset_token = _generate_uuid()
            self._db.update_user(user_id, reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError("No result found")

    def update_password(self, password: str, reset_token: str) -> None:
        """ Update a user's password """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            if user.reset_token != reset_token:
                raise ValueError
            hashed_password = _hash_password(password)
            self._db.update_user(user.id, hashed_password=hashed_password,
                                 reset_token=None)
        except NoResultFound:
            raise ValueError
