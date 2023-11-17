import pytest
import requests
from dotenv import load_dotenv,find_dotenv
import os
from app.shared_vars import BASE_URL

SECRET_FILE = os.environ.get('SECRET_FILE')
if SECRET_FILE:
    with open(SECRET_FILE, 'r') as secret_file:
        for line in secret_file:
            line = line.strip()
            if '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()
            else:
                print(f"Skipping line in secret file: {line}")

# You can now access environment variables directly
TEST_EMAIL = os.getenv("TEST_EMAIL")
TEST_PASSWORD = os.getenv("TEST_PASSWORD")
TEST_EMAIL_LOCKED = os.getenv("TEST_EMAIL_LOCKED")
TEST_EMAIL_UNVERIFIED = os.getenv("TEST_EMAIL_UNVERIFIED")

@pytest.fixture
def test_login_data():
    # masked email and password in env file for testing purposes
    valid_login_data = {"email": TEST_EMAIL, "password": TEST_PASSWORD}
    unverified_email_data ={"email": TEST_EMAIL_UNVERIFIED, "password": TEST_PASSWORD}
    invalid_login_data = {"email": "invalid@example.com", "password": "invalid_password"}
    locked_out_user = {"email": TEST_EMAIL_LOCKED, "password": TEST_PASSWORD}
    return {
        "valid_login_data": valid_login_data,
        "invalid_login_data": invalid_login_data,
        "locked_out_user": locked_out_user,
        "unverified_email_data": unverified_email_data
    }

# #test for valid user login (credentials exists in database)
# def test_login_success(test_login_data):
#     # Test a successful login request
#     response = requests.post(BASE_URL + '/login', json=test_login_data["valid_login_data"])
#     json_data = response.json()

#     assert response.status_code == 200
#     assert "success" in json_data
#     assert json_data["success"] is True

#test for invalid user login (credentials does not exists in database)
def test_login_invalid_user(test_login_data):
    # Test a login request with an invalid user
    response = requests.post(BASE_URL + '/login', json=test_login_data["invalid_login_data"])
    json_data = response.json()
    assert response.status_code == 404
    assert "success" in json_data
    assert json_data["success"] is False
    assert "error" in json_data
    assert json_data["error"] == "No such user"

#test for a user when thier account is being locked
def test_login_locked_out_user(test_login_data):
    # Test a login request for a locked-out user
    response = requests.post(BASE_URL + '/login', json=test_login_data["locked_out_user"])
    json_data = response.json()

    assert response.status_code == 401
    assert "success" in json_data
    assert json_data["success"] is False
    assert "error" in json_data
    assert json_data["error"] == "User Account Locked. Please contact Admin"

#do not test this function too much as user will be locked out
#if it is locked enable the user back in admin panel.
# def test_login_invalid_password(test_login_data):
#     # Test a login request with an invalid password
#     invalid_password_data = {"email":TEST_EMAIL, "password": "incorrect_password"}
#     response = requests.post(BASE_URL + '/login', json=invalid_password_data)
#     json_data = response.json()

#     assert response.status_code == 401
#     assert "success" in json_data
#     assert json_data["success"] is False
#     assert "error" in json_data
#     assert json_data["error"] == "Authentication failed"

#test for user email not verified unable to login
def test_login_email_not_verified(test_login_data):
    # Test a login request for a user with an unverified email
    response = requests.post(BASE_URL + '/login', json=test_login_data["unverified_email_data"])
    json_data = response.json()
    assert response.status_code == 401
    assert "success" in json_data
    assert json_data["success"] is False
    assert "error" in json_data
    assert json_data["error"] == "Email is not verified. Please verify your email before logging in."

