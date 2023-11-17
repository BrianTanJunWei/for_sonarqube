import pytest
import requests
import os,io
import sys
from dotenv import load_dotenv
# Now you can import 'app' from the 'server' module
from server import app
from io import BytesIO
from PIL import Image, ImageDraw
# Define the base URL for your API


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
#You can use the 'requests' library to make HTTP requests to your API
# Load environment variables
# load_dotenv()

# Define test data for authentication (you can replace these with actual test data)
TEST_SESSION_ID = os.getenv("TEST_SESSION_ID")
TEST_USER_ROLE = os.getenv("TEST_USER_ROLE")

@pytest.fixture
def authenticated_client():
    client = app.test_client()

    with client.session_transaction() as sess:
        # Set the session data for an authenticated user
        sess['user_id'] = TEST_SESSION_ID
        sess['user_role'] = TEST_USER_ROLE
    return client

@pytest.fixture
def unauthenticated_client():
    client = app.test_client()

    with client.session_transaction() as sess:
        # Set the session data for an authenticated user
        sess['user_id'] = 'x'
        sess['user_role'] = 'x'

    return client
#check for authenticated personnel
# def test_update_profile_success(authenticated_client):
#     # Make a POST request to the UpdateProfileAPI
#     response = authenticated_client.post('/updateProfile', data={'name': 'tzw99', 'phonenumber': '83990696'})

#     # Check the response status code
#     assert response.status_code == 200  # Assuming a successful update should return HTTP 200

#     # Check the response content for success
#     expected_response = {"success": True}
#     assert response.get_json() == expected_response
# #Test for unauthenticated personnel

# def test_update_profile_wrong_phonenumberformat(authenticated_client):
#     # Make a POST request to the UpdateProfileAPI without authentication
#     response = authenticated_client.post('/updateProfile', data={'name': '', 'phonenumber': 'xxx'})
    
#     # Check the response status code
#     assert response.status_code == 400  # Assuming an unauthenticated user should return HTTP 401
    
#     # Check the response content for success
#     expected_response = {"error": 'Phone number must be numeric'}
#     assert response.get_json() == expected_response

# def testImage():
#     # Create a blank image with a white background
#     width, height = 200, 200
#     image = Image.new("RGB", (width, height), "white")

#     # Create a drawing context
#     draw = ImageDraw.Draw(image)

#     # Draw a red rectangle on the image
#     draw.rectangle([50, 50, 150, 150], fill="red")

#     # Save the image as bytes in a variable
#     image_data = BytesIO()
#     image.save(image_data, format="PNG")
#     image_data.seek(0)

#     return image_data

# #update wrong image file format
# def test_update_profile_wrong_pictureformat(authenticated_client):
#     image_data = testImage()
#     image_file = io.BytesIO(image_data.read())
#      # Create a dictionary for form data
#     update_data_test = {
#         'name': 'tzw99',
#         'phonenumber': '83990696',
#     }

#     # Append the image file to the form data
#     update_data_test['profilePicture'] = (image_file, 'image.gif')

#     response = authenticated_client.post('/updateProfile', data=update_data_test)
#     # Check the response status code
#     print(response)
#     assert response.status_code == 400
   
#     # Check the response content for success
#     expected_response = {"error": 'Invalid file format. Allowed formats: JPEG, JPG, PNG'}
   
#     assert response.get_json() == expected_response


# #update correct image file format
# def test_update_profile_correct_pictureformat(authenticated_client):
#     image_data = testImage()
#     image_file = io.BytesIO(image_data.read())
#      # Create a dictionary for form data
#     update_data_test = {
#         'name': 'tzw99',
#         'phonenumber': '83990696',
#     }

#     # Append the image file to the form data
#     update_data_test['profilePicture'] = (image_file, 'image.png')

#     response = authenticated_client.post('/updateProfile', data=update_data_test)
#     # Check the response status code
#     print(response)
#     assert response.status_code == 200
   
#     #Check the response content for success
#     expected_response = {"success": True}
#     assert response.get_json() == expected_response

# def test_get_profile_authenticated(authenticated_client):
#     # The authenticated_client fixture provides a test client with the session data set.
#     response = authenticated_client.get('/profile')
    
#     # Check if the response status code is 200 (success)
#     assert response.status_code == 200

#     # You can also check specific data in the response JSON
#     profile_data = response.get_json()
#     assert 'name' in profile_data
#     assert 'age' in profile_data
#     assert 'phonenumber' in profile_data
#     assert 'email' in profile_data
#     assert 'profilePicture' in profile_data

def test_get_profile_unauthenticated(unauthenticated_client):
    # Create a test client for your app
    client = app.test_client()
    
    # Test getting the profile for an unauthenticated user
    response = unauthenticated_client.get('/profile')
    
    # Check if the response status code is 404 (unauthenticated)
    assert response.status_code == 404

