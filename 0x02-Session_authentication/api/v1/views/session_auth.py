#!/usr/bin/env python3
"""Session authentication module"""
import os
from flask import jsonify, request, make_response
from api.v1.views import app_views
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login() -> str:
    """ POST /api/v1/auth_session/login"""
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None or email == '':
        return jsonify({"error": "email missing"}), 400
    if password is None or password == '':
        return jsonify({"error": "password missing"}), 400
    user = User.search({'email': email})
    if user is None or user == []:
        return jsonify({"error": "no user found for this email"}), 404
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    user_json = user.to_json()
    response = make_response(jsonify(user_json), 200)
    cookie_name = os.getenv('SESSION_NAME')
    response.set_cookie(cookie_name, session_id)

    return response
