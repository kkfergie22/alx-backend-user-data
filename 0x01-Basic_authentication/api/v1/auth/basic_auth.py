#!/usr/bin/env python3

"""Module of Basic Authentication"""
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar, Tuple
import base64


class BasicAuth(Auth):
    """BasicAuth class"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Extract base64 authorization header
        Args:
            authorization_header (str): authorization header
        Returns:
            str: base64 part of the authorization header
        """
        if authorization_header is None:
            return None
        if type(authorization_header) != str:
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """Decode base64 authorization header
        Args:
            base64_authorization_header (str): base64 authorization header
        Returns:
            str: decoded value of the base64 authorization header
        """
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) != str:
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """Extract user credentials
        Args:
            decoded_base64_authorization_header (str): decoded value of the
            base64 authorization header
        Returns:
            tuple: user email, user password
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if type(decoded_base64_authorization_header) != str:
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        return tuple(decoded_base64_authorization_header.split(':', 1))

    # def user_object_from_credentials(self, user_email: str, user_pwd: str
    #                                  ) -> TypeVar('User'):
    #     """User object from credentials
    #     Args:
    #         user_email (str): user email address (unique) to search
    #         user_pwd (str): user password associated with the email
    #     Returns:
    #         TypeVar('User'): user instance found or None
    #     """
    #     if user_email is None or type(user_email) != str:
    #         return None
    #     if user_pwd is None or type(user_pwd) != str:
    #         return None
    #     try:
    #         users = User.search({'email': user_email})
    #     except Exception:
    #         return None
    #     for user in users:
    #         if user.is_valid_password(user_pwd):
    #             return user
    #     return None

    # def current_user(self, request=None) -> TypeVar('User'):
    #     """Current user
    #     Args:
    #         request (Request): Flask request object. Defaults to None.
    #     Returns:
    #         TypeVar('User'): user instance or None
    #     """
    #     auth_header = self.authorization_header(request)
    #     base64_auth_header = self.extract_base64_authorization_header(
    #         auth_header)
    #     decoded_auth_header = self.decode_base64_authorization_header(
    #         base64_auth_header)
    #     user_credentials = self.extract_user_credentials(decoded_auth_header)
    #     return self.user_object_from_credentials(user_credentials[0],
    #                                              user_credentials[1])
