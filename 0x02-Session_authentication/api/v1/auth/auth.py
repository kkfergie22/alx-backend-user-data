#!/usr/bin/env python3
"""Auth class to manage the API authentication"""

from flask import request
from typing import List, TypeVar


class Auth:
    """Auth class to manage the API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Require authentication
        Args:
            path (str): path to authenticate
            excluded_paths (List[str]): list of paths not to authenticate
        Returns:
            bool: True if authentication is required, False otherwise
        """
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        if path[-1] != '/':
            path += '/'
        for p in excluded_paths:
            if p[-1] == '*':
                if path.startswith(p[:-1]):
                    return False
            elif path == p:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Authorization header
        Args:
            request (Request): Flask request object. Defaults to None.
        Returns:
            str: value of the Authorization header
        """
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """Current user
        Args:
            request (Request): Flask request object. Defaults to None.
        Returns:
            TypeVar('User'): user instance
        """
        return None
