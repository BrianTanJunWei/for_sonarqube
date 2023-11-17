import pytest
import io
import requests
from app.shared_vars import BASE_URL
from io import BytesIO
from PIL import Image, ImageDraw

@pytest.fixture
def test_register_data():
    valid_register_data = {
        'name': 'TestedValidUser',
        'phoneNumber': '86666666',
        'age': '22',
        'email': 'validuser@hotmail.com',
        'password': 'tzw99556_P',
        'role': 'Buyer',
        
    }
    invalid_register_data = {
        'name': 'Invalid User',
        'phoneNumber': 'invalid_phonenumber',
        'age': 'invalid_age',
        'email': 'invalid_email',
        'password': 'invalid_password',
        'role': 'InvalidRole',
        'profilePicture': '',
    }
    emailexists_register_data = {
        'name': 'DeleteUser',
        'phoneNumber': '88888888',
        'age': '22',
        'email': 'tanzongwei1998@gmail.com',
        'password': 'tzw99556_P',
        'role': 'Buyer',
        'profilePicture': '',
    }
    nameexists_register_data = {
        'name': 'mikh',
        'phoneNumber': '83333333',
        'age': '23',
        'email': 'mik@hotmail.com',
        'password': 'tzw99556_P',
        'role': 'Buyer',
        'profilePicture': '',
    }
    # phonenumberexists_register_data = {
    #     'name': 'xxx',
    #     'phoneNumber': '96272708',
    #     'age': '22',
    #     'email': 's882@hotmail.com',
    #     'password': 'tzw99556_P',
    #     'role': 'Buyer',
    #     'profilePicture': '',
    # }
    incorrectpictureformat_register_data = {
        'name': 'picture',
        'phoneNumber': '95555555',
        'age': '22',
        'email': 'shad882@hotmail.com',
        'password': 'tzw99556_P',
        'role': 'Seller',
    }

    return {
        'valid_register_data': valid_register_data,
        'invalid_register_data': invalid_register_data,
        #  'phonenumberexists_register_data' : phonenumberexists_register_data,
         'nameexists_register_data': nameexists_register_data,
        'emailexists_register_data': emailexists_register_data,
        'incorrectpicture_registerdata': incorrectpictureformat_register_data
    }

def testImage():
    # Create a blank image with a white background
    width, height = 200, 200
    image = Image.new("RGB", (width, height), "white")

    # Create a drawing context
    draw = ImageDraw.Draw(image)

    # Draw a red rectangle on the image
    draw.rectangle([50, 50, 150, 150], fill="red")

    # Save the image as bytes in a variable
    image_data = BytesIO()
    image.save(image_data, format="PNG")
    image_data.seek(0)

    return image_data

def test_register_incorrectpicture_format(test_register_data):
    image_data = testImage()
    image_file = io.BytesIO(image_data.read())
    response = requests.post(BASE_URL + '/register', data=test_register_data['incorrectpicture_registerdata'], files={'profilePicture': ('image.gif', image_file)})
    json_data = response.json()
    print(json_data)
    assert response.status_code == 400
    assert 'success' in json_data
    assert json_data['success'] is False
    assert 'error' in json_data

    # Ensure that the error message for phone number and age validation is present
    assert 'Invalid file format. Allowed formats: .jpg, .jpeg, .png' in json_data['error']

# Test for success registration data and delete data afterwards.
def test_registration_success(test_register_data):
    image_data = testImage()
    image_file = io.BytesIO(image_data.read())
    response = requests.post(BASE_URL + '/register', data=test_register_data['valid_register_data'],files={'profilePicture': ('image.png', image_file)})
    json_data = response.json()

    assert response.status_code == 200
    assert 'success' in json_data
    assert json_data['success'] is True

    # Step 2: Delete the registered user
    # Assuming the registered user's email is in test_register_data['valid_register_data']['email']
    email = test_register_data['valid_register_data']['email']
    delete_user_data = {'email': email}
    delete_response = requests.post(BASE_URL + '/delete', data=delete_user_data)
    delete_json_data = delete_response.json()
      # Check if user deletion was successful
    assert delete_response.status_code == 200
    assert 'success' in delete_json_data
    assert delete_json_data['success'] is True

# #test for phone exists
# def test_registration_phone_exists_invalid_data(test_register_data):
#     response = requests.post(BASE_URL + '/register', data=test_register_data['phonenumberexists_register_data'])
#     json_data = response.json()

#     assert response.status_code == 400
#     assert 'success' in json_data
#     assert json_data['success'] is False
#     assert 'error' in json_data

#     # Ensure that the error message for phone number and age validation is present
#     assert 'Phone number already exists' in json_data['error']

#test for name exists
def test_registration_name_exists_invalid_data(test_register_data):
    response = requests.post(BASE_URL + '/register', data=test_register_data['nameexists_register_data'])
    json_data = response.json()

    assert response.status_code == 400
    assert 'success' in json_data
    assert json_data['success'] is False
    assert 'error' in json_data

    # Ensure that the error message for phone number and age validation is present
    assert 'Name already exists' in json_data['error']


#test for email exists
def test_registration_email_exists_invalid_data(test_register_data):
    response = requests.post(BASE_URL + '/register', data=test_register_data['emailexists_register_data'])
    json_data = response.json()

    assert response.status_code == 400
    assert 'success' in json_data
    assert json_data['success'] is False
    assert 'error' in json_data

    # Ensure that the error message for phone number and age validation is present
    assert 'Email already exists' in json_data['error']


#invalid data test
def test_registration_invalid_data(test_register_data):
    response = requests.post(BASE_URL + '/register', data=test_register_data['invalid_register_data'])
    json_data = response.json()

    assert response.status_code == 400
    assert 'success' in json_data
    assert json_data['success'] is False
    assert 'error' in json_data

    # Ensure that the error message for phone number and age validation is present
    assert 'Phone number and age must be valid numbers' in json_data['error']

