import unittest
import requests
import io,os
from io import BytesIO
from PIL import Image, ImageDraw
from dotenv import load_dotenv
from app.config.config import db
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
TEST_SELLER_USERID = os.getenv("TEST_SELLER_USERID")

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

class TestAddProductAPI(unittest.TestCase):
    def test_add_product(self):
        #Create dummy image and send as a .png file
        image_data = testImage()
        image_file = io.BytesIO(image_data.read())
        # Define the dummy product data
        test_product_data = {
            'ProductName': 'Dummy Product',
            'PID': 'PROD9',
            'quantity': 10,
            'cost': '9.99',
            'description': 'A test product',
            'productType': 'Sports',
            'sellerUID': 'abc123',
            'availability': 'In Stock'
        }
        # Create a file-like object from the image data
        
        # Send a POST request to your API to add the dummy product
        response = requests.post(f'{BASE_URL}/add-product', data=test_product_data, files={'ProductPicture': ('image.png', image_file)})

        json_data = response.json()
        # Check if the response status code is 200 (success)
        self.assertEqual(response.status_code, 200)

        # Check if the response message indicates success
        
        self.assertTrue(json_data["success"])

    def test_add_invalid_product(self):
        # Define the invalid product data
        test_product_data = {
            'ProductName': 'Invalid Product',
            'PID': 'PROD0',
            'quantity': 0,
            'cost': '0',
            'description': '',
            'productType': 'Sports',
            'sellerUID': 'abc123',
            'availability': 'In Stock'
        }

        # Send a POST request to your API to add the dummy product
        response = requests.post(f'{BASE_URL}/add-product', data=test_product_data)

        # Check if the response status code is 200 (success)
        self.assertEqual(response.status_code, 404)

        # Check if the response message indicates success
        json_data = response.json()
        expected_message = "Invalid Product Parameters! Please try again!"
        self.assertIn(expected_message, json_data["message"])

    def test_invalid_product_image(self):
        image_data = testImage()
        image_file = io.BytesIO(image_data.read())
        # Define the dummy product data
        test_product_data = {
            'ProductName': 'Dummy Product',
            'PID': 'PROD9',
            'quantity': 10,
            'cost': '9.99',
            'description': 'A test product',
            'productType': 'Sports',
            'sellerUID': 'abc123',
            'availability': 'In Stock'
        }

        # Send a POST request to your API to add the dummy product
        response = requests.post(f'{BASE_URL}/add-product', data=test_product_data, files={'ProductPicture': ('image.gif', image_file)})

        # Check if the response status code is 200 (success)
        self.assertEqual(response.status_code, 404)

        # Check if the response message indicates success
        json_data = response.json()
        expected_message = "Invalid file format. Only .png, .jpg, and .jpeg files are allowed."
        self.assertIn(expected_message, json_data["message"])

    def test_Invalid_image_file(self):
        # Define the dummy product data
        test_product_data = {
            'ProductName': 'Dummy Product',
            'PID': 'PROD9',
            'quantity': 10,
            'cost': '9.99',
            'ProductPicture': "Test Image",
            'description': 'A test product',
            'productType': 'Sports',
            'sellerUID': 'abc123',
            'availability': 'In Stock'
        }
        # Create a file-like object from the image data
        
        # Send a POST request to your API to add the dummy product
        response = requests.post(f'{BASE_URL}/add-product', data=test_product_data)

        json_data = response.json()
        # Check if the response status code is 200 (success)
        self.assertEqual(response.status_code, 404)
        expected_message ="Something went wrong with uploading image. Please try again!"
        self.assertIn(expected_message, json_data["message"])

class TestGetProductAPI(unittest.TestCase):
    def test_get_existing_product(self):
        # Define an existing product ID
        productId = "PROD9"
        
        # Send a GET request to retrieve the product
        response = requests.get(f'{BASE_URL}/get-product/{productId}')
        
        # Check if the response status code is 200 (success)
        self.assertEqual(response.status_code, 200)
        
        # Check if the response contains product data
        product_data = response.json()
        self.assertTrue('ProductName' in product_data)
        
    def test_get_non_existing_product(self):
        # Define a non-existing product ID
        product_id = 'PROD0'  # Replace with a product ID that doesn't exist in your database
        
        # Send a GET request to retrieve the product
        response = requests.get(f'{BASE_URL}/get-product/{product_id}')
        
        # Check if the response status code is 404 (not found)
        self.assertEqual(response.status_code, 404)
        
        # Check if the response contains an error message indicating the product was not found
        response_data = response.json()
        self.assertTrue('error' in response_data)
        self.assertEqual(response_data['error'], 'Product not found')

    def test_get_invalid_product(self):
        # Create a test case for deleting an invalid product
        productId = "123456"
        response = requests.get(f'{BASE_URL}/get-product/{productId}')
        json_data = response.json()

        # Check if the response status code is 404 (not found)
        self.assertEqual(response.status_code, 404)
        print(json_data)
        # Check if the response message indicates that the product was not found
        self.assertEqual(json_data['error'], 'Error! Invalid product')

class TestSellerProductsAPI(unittest.TestCase):
    def test_seller_products(self):
        # using test product seller ID
        seller_uid = 'abc123'

        # Send a GET request to the API
        response = requests.get(f'{BASE_URL}/Sellerproducts?seller_uid={seller_uid}')

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)
        # Check if the response is not an empty list
        self.assertNotEqual(response.json(), [])  

    def test_seller_products_invalid_seller(self):
        # Send a GET request with a seller UID that has no products
        seller_uid = 'xyz798'
        response = requests.get(f'{BASE_URL}/Sellerproducts?seller_uid={seller_uid}')

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)
        # Assert that the response contains an empty list (no products)
        self.assertEqual(response.json(), [])

class TestEditProductAPI(unittest.TestCase):
    def test_edit_product(self):
        # Create a dummy product and send as a .png file
        image_data = testImage()
        image_file = io.BytesIO(image_data.read())

        # Define the dummy product data to be edited
        product_id = 'PROD9'
        updated_data = {
            'ProductName': 'Updated Dummy Product',
            'quantity': 20,
            'cost': '19.99',
            'description': 'An updated Dummy product',
            'productType': 'Computer',
            'availability': 'In Stock'
        }
        
        # Send a POST request to edit the product with the updated data and image
        response = requests.post(f'{BASE_URL}/edit-product/{product_id}', data=updated_data, files={'ProductPicture': ('image.png', image_file)})

        # Check if the response status code is 200 (success)
        self.assertEqual(response.status_code, 200)

        # Check if the response message indicates success
        json_data = response.json()
        self.assertIn("Product updated successfully", json_data["message"])

    def test_edit_non_existing_product(self):
        # Define a non-existing product ID
        product_id = 'PROD0'

        # Define the updated data (does not matter in this case)
        updated_data = {
            'ProductName': 'Updated Product',
            'quantity': 20,
            'cost': '19.99',
            'description': 'An updated product',
            'productType': 'Electronics',
            'availability': 'In Stock'
        }

        # Send a POST request to edit the non-existing product
        response = requests.post(f'{BASE_URL}/edit-product/{product_id}', data=updated_data)

        # Check if the response status code is 404 (not found)
        self.assertEqual(response.status_code, 404)

        # Check if the response message indicates that the product was not found
        json_data = response.json()
        self.assertIn("Product not found", json_data["error"])

    def test_edit_product_with_missing_fields(self):
        # Define an existing product ID
        product_id = 'PROD1'

        # Define the updated data with some missing fields
        updated_data = {
            'ProductName': 'Updated dummy Product',
            'quantity': 20,
            'description': 'An updated product',
            'productType': 'Electronics',
            'availability': 'In Stock'
        }

        # Send a POST request to edit the product with missing fields
        response = requests.post(f'{BASE_URL}/edit-product/{product_id}', data=updated_data)

        # Check if the response status code is 400 (bad request)
        self.assertEqual(response.status_code, 404)

        # Check if the response message indicates missing form fields
        json_data = response.json()
        self.assertIn("Missing form fields", json_data["error"])

    def test_edit_product_invalid_product_id(self):
        # Create a dummy product and send as a .png file
        image_data = testImage()
        image_file = io.BytesIO(image_data.read())

        # Define the dummy product data to be edited
        product_id = '123456'
        updated_data = {
            'ProductName': 'Updated Dummy Product',
            'quantity': 20,
            'cost': '19.99',
            'description': 'An updated Dummy product',
            'productType': 'Computer',
            'availability': 'In Stock'
        }

        # Send a POST request to edit the product with the updated data and image
        response = requests.post(f'{BASE_URL}/edit-product/{product_id}', data=updated_data, files={'ProductPicture': ('image.png', image_file)})

        # Check if the response status code is 200 (success)
        self.assertEqual(response.status_code, 404)

        # Check if the response message indicates success
        json_data = response.json()
        self.assertIn("Error! Invalid product", json_data["message"])

    def test_edit_product_invalid_product_image(self):
        image_data = testImage()
        image_file = io.BytesIO(image_data.read())
        # Define the dummy product data
        product_id = 'PROD9'
        updated_data = {
            'ProductName': 'Updated Dummy Product',
            'quantity': 40,
            'cost': '200.99',
            'description': 'An updated Dummy product',
            'productType': 'Computer',
            'availability': 'In Stock'
        }

        # Send a POST request to your API to add the dummy product
        response = requests.post(f'{BASE_URL}/edit-product/{product_id}', data=updated_data, files={'ProductPicture': ('image.xml', image_file)})

        # Check if the response status code is 200 (success)
        self.assertEqual(response.status_code, 404)

        # Check if the response message indicates success
        json_data = response.json()
        print(json_data)
        expected_message = "Invalid file format. Only .png, .jpg, and .jpeg files are allowed."
        self.assertIn(expected_message, json_data["message"])
    

class TestDeleteProductAPI(unittest.TestCase):
    def test_delete_existing_product(self):
        # Create a test case for deleting an existing product
        productId = "PROD9"
        response = requests.delete(f'{BASE_URL}/delete-product/{productId}')
        json_data = response.json()

        # Check if the response status code is 200 (success)
        self.assertEqual(response.status_code, 200)

        # Check if the response message indicates success
        self.assertIn("deleted successfully", json_data["message"])

    def test_delete_non_existing_product(self):
        # Create a test case for deleting a non-existing product
        productId = "PROD1"
        response = requests.delete(f'{BASE_URL}/delete-product/{productId}')
        json_data = response.json()

        # Check if the response status code is 404 (not found)
        self.assertEqual(response.status_code, 404)

        # Check if the response message indicates that the product was not found
        expected_message = f"No product found with ID {productId}"
        self.assertIn(expected_message, json_data["message"])

    def test_delete_invalid_product(self):
        # Create a test case for deleting an invalid product
        productId = "123456"
        response = requests.delete(f'{BASE_URL}/delete-product/{productId}')
        json_data = response.json()

        # Check if the response status code is 404 (not found)
        self.assertEqual(response.status_code, 404)

        # Check if the response message indicates that the product was not found
        self.assertIn("Error! Invalid product", json_data["message"])


class TestNotificationsAPI(unittest.TestCase):
    def test_successful_get_notifications(self):
        userid= TEST_SELLER_USERID
        # Test a successful request for notifications
        response = requests.get(f"{BASE_URL}/get_notifications?seller_uid={userid}")
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertIsNotNone(json_data)  # Assert that the data is not empty

        # Check if the response data contains specific keys
        for item in json_data:
            self.assertIn("NotifID", item)
            self.assertIn("Product", item)
            self.assertIn("BuyerEmail", item)
            self.assertIn("Time", item)
            self.assertIn("Quantity", item)

    def test_missing_seller_uid(self):
        # Test when seller_uid is missing
        response = requests.get(f"{BASE_URL}/get_notifications")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"error": "SellerID is required"})

class TestDeleteNotificationAPI(unittest.TestCase):
    def Create_test_notification(self):
        userId = TEST_SELLER_USERID
        notificationId = "TESTEST"
        notification_ref = db.reference(f'Notifications/{userId}/{notificationId}')
        notif_to_add = {
            "product": "Dummy Notification",
            "buyer": "Dummy Buyer",
            "quantity": 20,
            "time": "2023-10-30 12:00:00"
        }
        notification_ref.set(notif_to_add)

    def test_successful_notification_deletion(self):
        self.Create_test_notification()
        # Function to push a dummy notification to the database
        userId = TEST_SELLER_USERID
        notificationId = "TESTEST"
        # Test a successful notification deletion

        response = requests.delete(f'{BASE_URL}/delete-notification/{userId}/{notificationId}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": f"Notification with ID {notificationId} deleted successfully"})

    def test_invalid_notification_id(self):
        # Test when an invalid notification ID is provided
        userId = TEST_SELLER_USERID
        notificationId = None
        response = requests.delete(f"{BASE_URL}/delete-notification/{userId}/{notificationId}")
        self.assertEqual(response.status_code, 404)
        json_data = response.json()
        # Check that the response contains a 404 status message
        self.assertIn(f"No notification found with ID {notificationId}", json_data["message"])


def test_suite():
    suite = unittest.TestSuite()

    #Add test cases in the desired order
    suite.addTest(unittest.makeSuite(TestAddProductAPI))
    suite.addTest(unittest.makeSuite(TestGetProductAPI))
    suite.addTest(unittest.makeSuite(TestSellerProductsAPI))
    suite.addTest(unittest.makeSuite(TestDeleteProductAPI))
    suite.addTest(unittest.makeSuite(TestNotificationsAPI))
    suite.addTest(unittest.makeSuite(TestDeleteNotificationAPI))

    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    test_suite_instance = test_suite()
    runner.run(test_suite_instance)
