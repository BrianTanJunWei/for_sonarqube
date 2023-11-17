import unittest
import requests
import os
from dotenv import load_dotenv
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
#load_dotenv()
TEST_SELLER_EMAIL = os.getenv("TEST_SELLER_EMAIL")

class TestGetAccountsAPI(unittest.TestCase):
    def test_get_user_accounts(self):
        # Send a GET request to the API
        response = requests.get(f'{BASE_URL}/get_accounts')

        # Check if the response status code is 200 (success)
        self.assertEqual(response.status_code, 200)

        # Check if the response contains user data
        user_data = response.json()
        # Check if the response data matches the expected data
        self.assertNotEqual(user_data, [])

class TestUpdateUserStatusAPI(unittest.TestCase):
    def test_update_user_status_successful(self):
        # Create a test user with an initial status
        user_data = {
            "userId": TEST_SELLER_EMAIL,
            "role": "Seller",
            "disabled": False
        }
        # Simulate the request to update the user status
        response = requests.post(f'{BASE_URL}/update_user_status', json=user_data)

        # Check if the response status code is 200 (success)
        self.assertEqual(response.status_code, 200)

        json_data = response.json()
        # Verify that the status has been updated
        self.assertTrue(json_data["success"])
        # if change was successful then unlock it back
        if (response.status_code == 200) and (json_data["success"] is True):
            # Reset user status
            user_data = {
                "userId": TEST_SELLER_EMAIL,
                "role": "Seller",
                "disabled": True
            }
            # Simulate the request to update the user status
            response = requests.post(f'{BASE_URL}/update_user_status', json=user_data)

    def test_update_user_status_missing_fields(self):
        # Test with missing fields in the request data
        user_data = { # Role and disabled values is missing
            "userId": TEST_SELLER_EMAIL
        }
        # Simulate the request to update the user status
        response = requests.post(f'{BASE_URL}/update_user_status', json=user_data)

        # Check if the response status code is 404 (missing fields)
        self.assertEqual(response.status_code, 404)
        # Verify that the response contains an error message
        response = response.json()
        self.assertIn("Missing fields. Please try again", response["error"])

    def test_update_user_status_invalid_user(self):
        # Test with an invalid user ID
        user_data = {
            "userId": "invaliduser@example.com",
            "role": "buyer",
            "disabled": True
        }
        # Simulate the request to update the user status
        response = requests.post(f'{BASE_URL}/update_user_status', json=user_data)

        # Check if the response status code is 404 (error)
        self.assertEqual(response.status_code, 404)

        # Verify that the response contains an error message
        response_json = response.json()
        self.assertIn("User does not exist!", response_json["error"])

class TestLoginLogsAPI(unittest.TestCase):
    def test_get_login_logs_successful(self):

        # Simulate a successful request to get login logs
        response = requests.get(f'{BASE_URL}/login_logs')

        # Check if the response status code is 200 (success)
        self.assertEqual(response.status_code, 200)
        # Verify the response content
        response_data = response.json()
        self.assertIsInstance(response_data, list)
        self.assertIsNot(response_data, [])  # Ensure the list is not empty

class TestTransactionLogsAPI(unittest.TestCase):
    def test_get_transaction_logs_successful(self):

        # Simulate a successful request to get login logs
        response = requests.get(f'{BASE_URL}/transaction_logs')

        # Check if the response status code is 200 (success)
        self.assertEqual(response.status_code, 200)
        # Verify the response content
        response_data = response.json()
        self.assertIsInstance(response_data, list)
        self.assertIsNot(response_data, [])  # Ensure the list is not empty      

def test_suite():
    suite = unittest.TestSuite()

    # Add test cases in the desired order
    suite.addTest(unittest.makeSuite(TestGetAccountsAPI))
    suite.addTest(unittest.makeSuite(TestUpdateUserStatusAPI))
    suite.addTest(unittest.makeSuite(TestLoginLogsAPI))
    suite.addTest(unittest.makeSuite(TestTransactionLogsAPI))

    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    test_suite_instance = test_suite()
    runner.run(test_suite_instance)