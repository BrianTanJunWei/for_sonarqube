import time
import requests

BASE_URL ="http://backend:5000/"
while True:
    try:
        response = requests.get(f'{BASE_URL}/get_accounts')
        responsecode = response.status_code

        # If the request was successful (status code 200), you can break out of the loop
        if responsecode == 200:
            break
    except requests.exceptions.RequestException:
        # Handle the exception (optional), and then sleep for a while before the next retry
        print("Failed to establish a connection. Retrying in 5 seconds...")
        time.sleep(5)