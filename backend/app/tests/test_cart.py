import pytest
import requests
from dotenv import load_dotenv
import io,os
from test_seller_page import testImage

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

BASE_URL = 'http://backend:5000'  # Change this to your app's URL

# You can now access environment variables directly
TEST_EMAIL = os.getenv("TEST_EMAIL")
TEST_PASSWORD = os.getenv("TEST_PASSWORD")
TEST_EMAIL_LOCKED = os.getenv("TEST_EMAIL_LOCKED")
TEST_EMAIL_UNVERIFIED = os.getenv("TEST_EMAIL_UNVERIFIED")

@pytest.fixture
def test_init():
    # Set up a variable within the fixture
    filter_term = "computer"
    data_failed = {"email": "120"}
    test_cart = "test_cart"
    data_array = {"filter_term":filter_term, "data_failed":data_failed, "test_cart":test_cart}
    
    # Yield the variable
    yield data_array

def test_add_to_cart(test_init):
    #Create dummy image and send as a .png file
    image_data = testImage()
    image_file = io.BytesIO(image_data.read())
    # Define the dummy product data
    test_product_data = {
        'ProductName': 'Cart Dummy Product',
        'PID': 'PROD101',
        'quantity': 10,
        'cost': '9.99',
        'description': 'A test cart product',
        'productType': 'Sports',
        'sellerUID': 'abc123',
        'status': 'In Stock'
    }

    test_cart_data = {
        'quantity': 1
    }
    # Create a file-like object from the image data
    
    # Send a POST request to your API to add the dummy product
    response = requests.post(f'{BASE_URL}/add-product', data=test_product_data, files={'ProductPicture': ('image.png', image_file)})
    
    # Check if the response status code is 200 (success)
    assert response.status_code == 200

    responsecart = requests.post(f'{BASE_URL}/add-to-cart/{test_init["test_cart"]}/{test_product_data["PID"]}', json=test_cart_data)
    assert responsecart.status_code == 200

def test_get_cart(test_init):
    responsecart = requests.get(f'{BASE_URL}/get-cart/{test_init["test_cart"]}')
    json_data = responsecart.json()
    # Product ID to check
    product_id_to_check = 'PROD101'

    # Check if the product_id is in the JSON data
    product_found = any(item['product_id'] == product_id_to_check for item in json_data)
    assert product_found
    assert responsecart.status_code == 200
    

def test_delete_from_cart(test_init):
    #Create dummy image and send as a .png file
    image_data = testImage()
    image_file = io.BytesIO(image_data.read())
    # Define the dummy product data
    test_product_data = {
        'ProductName': 'Cart Dummy Product',
        'PID': 'PROD101',
        'quantity': 10,
        'cost': '9.99',
        'description': 'A test cart product',
        'productType': 'Sports',
        'sellerUID': 'abc123',
        'status': 'In Stock'
    }

    test_cart_data = {
        'quantity': 1
    }
    # Create a file-like object from the image data
    
    # Send a POST request to your API to add the dummy product
    response = requests.post(f'{BASE_URL}/add-product', data=test_product_data, files={'ProductPicture': ('image.png', image_file)})
    
    # Check if the response status code is 200 (success)
    assert response.status_code == 200

    responsecart = requests.post(f'{BASE_URL}/add-to-cart/{test_init["test_cart"]}/{test_product_data["PID"]}', json=test_cart_data)
    assert responsecart.status_code == 200

    deleteresponse = requests.delete((f'{BASE_URL}/delete-from-cart/{test_init["test_cart"]}/{test_product_data["PID"]}'))
    assert deleteresponse.status_code == 200

