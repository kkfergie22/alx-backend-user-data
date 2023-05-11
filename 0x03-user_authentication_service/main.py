#!/usr/bin/env python3

"Main module"
import requests

localhost_url = "http://0.0.0.0:5000"


def register_user(email: str, password: str) -> None:
    """Test user registration"""
    data = {"email": email, "password": password}
    response = requests.post(f"{localhost_url}/users", data)
    response_data = response.json()
    assert response.status_code == 200
    assert email in response_data
    assert password in response_data


def log_in_wrong_password(email: str, password: str) -> None:
    """"""
    data = {"email": email, "password": password}
    response = requests.post(f"{localhost_url}/sessions", data)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """"""
    data = {"email": email, "password": password}
    response = requests.post(f"{localhost_url}/sessions", data)
    response_data = response.json()
    assert response.status_code == 200
    assert email in response_data
    assert "session_id" in response_data
    return response_data["session_id"]


def profile_unlogged() -> None:
    """Tests profile unlogged"""
    response = requests.get(f"{localhost_url}/profile")
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """Tests profile logged"""
    cookies = {"session_id": session_id}
    response = requests.get(f"{localhost_url}/profile", cookies=cookies)
    response_data = response.json()
    assert response.status_code == 200
    assert "email" in response_data
    assert "created_at" in response_data
    assert "updated_at" in response_data


def log_out(session_id: str) -> None:
    """Tests logout"""
    cookies = {"session_id": session_id}
    response = requests.delete(f"{localhost_url}/sessions", cookies=cookies)
    assert response.status_code == 302


def reset_password_token(email: str) -> str:
    """Tests password reset"""
    data = {"email": email}
    response = requests.post(f"{localhost_url}/reset_password", data)
    response_data = response.json()
    assert response.status_code == 200
    assert "reset_token" in response_data
    return response_data["reset_token"]


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Tests update password"""
    data = {"email": email, "reset_token": reset_token,
            "new_password": new_password}
    response = requests.put(f"{localhost_url}/reset_password", data)
    response_data = response.json()
    assert response.status_code == 200
    assert "email" in response_data
    assert "message" in response_data


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
