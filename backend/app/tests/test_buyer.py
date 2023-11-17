import pytest
import requests
from dotenv import load_dotenv
import os
# from app.config.config import app

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
    data_array = {"filter_term":filter_term, "data_failed":data_failed}
    # Yield the variable
    yield data_array

def test_fetch_all_products_success():
    # Create a test case for a successful password reset request
    # data = {"email": "tanzongwei1998@gmail.com"}  # Replace with a valid email
    response = requests.get(BASE_URL+"/FetchAllProducts")
    json_data = response.json()
    # print(json_data)

    # Check if the response status code is 200 (success)
    assert response.status_code == 200

def test_fetch_filtered_products(test_init):
    # Create a test case for a failed password reset request
    response = requests.get(BASE_URL+'/FetchFilteredProducts/' +test_init["filter_term"])
    json_data = response.json()
    # print(json_data)
    assert response.status_code == 200

def test_fetch_filtered_products_failed(test_init):
    response = requests.get(BASE_URL+'/FetchFilteredProducts/' +"failed_search")
    json_data = response.json()
    print(json_data)
    # Check if the response status code is a 400-level error (e.g., 400 Bad Request)
    assert 400 <= response.status_code < 500
    # Check if the response message indicates failure