import pytest
import requests
from dotenv import load_dotenv
import os
from server import app
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
# load_dotenv()

# You can now access environment variables directly
TEST_EMAIL = os.getenv("TEST_EMAIL")
TEST_PASSWORD = os.getenv("TEST_PASSWORD")
TEST_EMAIL_LOCKED = os.getenv("TEST_EMAIL_LOCKED")
TEST_EMAIL_UNVERIFIED = os.getenv("TEST_EMAIL_UNVERIFIED")
NEW_PASSWORD = os.getenv("NEW_PASSWORD")
# Define test data for authentication (you can replace these with actual test data)
TEST_SESSION_ID = os.getenv("TEST_SESSION_ID")
TEST_USER_ROLE = os.getenv("TEST_USER_ROLE")
TEST_FORGETEMAIL = os.getenv("TEST_FORGETEMAIL")

@pytest.fixture
def unauthenticated_client():
    client = app.test_client()

    with client.session_transaction() as sess:
        # Set the session data for an authenticated user
        sess['user_id'] = "xxxxx"
        sess['user_role'] = "xxxxx"

    return client

@pytest.fixture
def authenticated_client():
    client = app.test_client()

    with client.session_transaction() as sess:
        # Set the session data for an authenticated user
        sess['user_id'] = TEST_SESSION_ID
        sess['user_role'] = TEST_USER_ROLE

    return client

@pytest.fixture
def test_init():
    # Set up a variable within the fixture
    data_success = {"email": TEST_FORGETEMAIL}
    data_failed = {"email": "120"}
    data_array = {"data_success":data_success, "data_failed":data_failed}
    # Yield the variable
    yield data_array

# # Define the test case for ChangePasswordAPI
# def test_change_password_successful(authenticated_client):
#     # Make a POST request to the ChangePasswordAPI
#     response = authenticated_client.post('/change_password', json={'currentPassword': TEST_PASSWORD, 'newPassword': NEW_PASSWORD})

#     # Check the response status code
#     assert response.status_code == 200

#     # Check the response content for success
#     expected_response = {'message': 'Password changed successfully'}
#     assert response.get_json() == expected_response


# # Define the test case for ChangePasswordAPI
# def test_change_password_wrongcurrentpassword(authenticated_client):
#     # Make a POST request to the ChangePasswordAPI
#     response = authenticated_client.post('/change_password', json={'currentPassword': 'wrongpass', 'newPassword': NEW_PASSWORD})
#     #check for wrong current password input fail
#     # Check the response status code
#     assert response.status_code == 500


# # Define the test case for ChangePasswordAPI
# def test_unauthenticated_client(unauthenticated_client):
#     # Make a POST request to the ChangePasswordAPI
#     response = unauthenticated_client.post('/change_password', json={'currentPassword': TEST_PASSWORD, 'newPassword': NEW_PASSWORD})
   
#     # Check the response status code    
#     assert response.status_code == 500

#     # Check the response content for success
#     expected_response = {'error': 'No user record found for the provided user ID: xxxxx.'}
#     assert response.get_json() == expected_response

def test_forgot_password_success(test_init):
    # Create a test case for a successful password reset request
    response = requests.post(BASE_URL+'/forgot-password', json=test_init["data_success"])
    json_data = response.json()
    
    print(json_data)
    # Check if the response status code is 200 (success)
    assert response.status_code == 200

    # Check if the response message indicates success
    assert "success" in json_data
    assert json_data["success"] is True

def test_forgot_password_failure(test_init):
    # Create a test case for a failed password reset request
    data = {"email": "120"}  # Replace with an invalid email
    response = requests.post(BASE_URL+'/forgot-password', json=test_init["data_failed"])
    json_data = response.json()
    # Check if the response status code is a 400-level error (e.g., 400 Bad Request)
    assert 400 <= response.status_code < 500
    # Check if the response message indicates failure
    assert "success" in json_data
    assert json_data["success"] is False



