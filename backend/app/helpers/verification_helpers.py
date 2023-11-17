from app.config.config import db,firebase_auth,auth

#check if email is verified in firebase auth template
def is_email_verified(id_token):
    account_info = firebase_auth.get_account_info(id_token)
    return account_info['users'][0]['emailVerified']

def check_concurrent_login(user_id, user_role):
    # Retrieve the existing session token from Firebase
    user_role_ref = db.reference(user_role).child(user_id)
    existing_session_token = user_role_ref.child('session_token').get()

    if existing_session_token:
        # A session token exists, indicating concurrent login
        return False
    else:
        # No existing session token, allow the login
        return True
    
def find_user_by_email(email):
    try:
        # Use Firebase Admin SDK to retrieve a user by email
        user = auth.get_user_by_email(email)
        return user  # User with the provided email exists
    except auth.UserNotFoundError:
        return None  # User with the provided email does not exist
    
def check_phone_number_exists(phone_number, role):
    try:
        # Define the top-level reference to your Firebase database
        ref = db.reference()

        # Determine the table name based on the role
        table_name = role  # Assuming the role will be "Seller" or "Buyer"

        table_ref = ref.child(table_name)

        # Get a list of users in the table
        users = table_ref.get()

        # Convert the phone number to a string and remove leading/trailing spaces
        phone_number = str(phone_number).strip()

        # Loop through the users and check if the phone number exists
        for user_id, user_data in users.items():
            if 'phonenumber' in user_data and user_data['phonenumber'].strip() == phone_number:
                return True  # Phone number exists in the database

        # If the loop completes without finding a matching phone number, it doesn't exist
        return False

    except Exception as e:
        # Handle exceptions or errors here
        print(f"An error occurred: {e}")
        return False  # You can return False or raise an exception as per your error handling strategy


   
def check_name_exists(name, role):
    try:
        # Define the top-level reference to your Firebase database
        ref = db.reference()

        # Determine the table name based on the role
        table_name = role  # Assuming the role will be "Seller" or "Buyer"

        table_ref = ref.child(table_name)

        # Get a list of users in the table
        users = table_ref.get()

        # Convert the phone number to a string and remove leading/trailing spaces
        name = str(name).strip()

        # Loop through the users and check if the phone number exists
        for user_id, user_data in users.items():
            if 'name' in user_data and user_data['name'].strip() == name:
                return True  # Phone number exists in the database

        # If the loop completes without finding a matching phone number, it doesn't exist
        return False

    except Exception as e:
        # Handle exceptions or errors here
        print(f"An error occurred: {e}")
        return False  # You can return False or raise an exception as per your error handling strategy


