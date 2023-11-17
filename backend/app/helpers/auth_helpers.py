from app.config.config import auth, db,datetime,pytz,timedelta,uuid
from app.shared_vars import login_attempt_counts,MAX_LOGIN_ATTEMPTS

# Function to check if a user is locked out due to too many failed login attempts
def is_locked_out(email):
    return login_attempt_counts.get(email, 0) >= MAX_LOGIN_ATTEMPTS

def check_lockout_status(email):
    try:
        # Get the user's UID from Firebase
        user = auth.get_user_by_email(email)
        user_uid = user.uid

        # Determine the user's role (e.g., Buyer or Seller)
        user_role = determine_user_role(user_uid)

        if user_role:
            # Get the user's status from the corresponding node
            user_ref = db.reference(user_role).child(user_uid)
            user_data = user_ref.get()
            
            if user_data and 'status' in user_data:
                return user_data['status']

    except Exception as e:
        # Handle any errors that may occur while checking lockout status
        print(f"Error checking lockout status: {str(e)}")
    
    # Default to False (locked) if an error occurs
    return False

def getCurrentSessionToken(user_id, user_role):
    user_status_ref = db.reference(user_role).child(user_id).child("session_token")
    return user_status_ref.get()


# Function to set lockout status in Firebase
def set_lockout_status(email):
    try:
        # Get the user's UID from Firebase
        user = auth.get_user_by_email(email)
        user_uid = user.uid

        # Determine the user's role (e.g., Buyer or Seller)
        user_role = determine_user_role(user_uid)

        if user_role:
            # Update the 'status' key to False in the corresponding node
            user_ref = db.reference(user_role).child(user_uid)
            user_ref.update({"status": False})

    except Exception as e:
        # Handle any errors that may occur while updating Firebase
        print(f"Error setting lockout status: {str(e)}")

def lock_user_products(email):
    try:
        # Get the user's ID from their email
        user = auth.get_user_by_email(email)
        user_uid = user.uid

        # Reference to the 'Products' table in Firebase
        products_ref = db.reference('Products')

        # Get all product IDs
        product_ids = products_ref.get()

        if product_ids:
            for product_id in product_ids:
                product_data = products_ref.child(product_id).get()

                # Check if the product's sellerUID matches the user_uid
                if product_data.get("sellerUID") == user_uid:
                    # Update the status to False
                    product_ref = products_ref.child(product_id)
                    product_ref.update({"status": False})
        return True

    except Exception as e:
        return False
    
def unlock_user_products(email):
    try:
        # Get the user's ID from their email
        user = auth.get_user_by_email(email)
        user_uid = user.uid

        # Reference to the 'Products' table in Firebase
        products_ref = db.reference('Products')

        # Get all product IDs
        product_ids = products_ref.get()

        if product_ids:
            for product_id in product_ids:
                product_data = products_ref.child(product_id).get()

                # Check if the product's sellerUID matches the user_uid
                if product_data.get("sellerUID") == user_uid:
                    # Update the status to False
                    product_ref = products_ref.child(product_id)
                    product_ref.update({"status": True})
        return True

    except Exception as e:
        return False


# Function to increment the login attempt count for a user
def increment_login_attempt(email):
    if email in login_attempt_counts:
        login_attempt_counts[email] += 1
    else:
        login_attempt_counts[email] = 1

# Function to reset the login attempt count for a user
def reset_login_attempt(email):
    if email in login_attempt_counts:
        login_attempt_counts[email] = 0

#determine the user role
def determine_user_role(user_id):
    buyer_user_ref = db.reference('Buyer').child(user_id)
    seller_user_ref = db.reference('Seller').child(user_id)
    admin_user_ref = db.reference('Admin').child(user_id)

    if buyer_user_ref.get():
        return 'Buyer'
    elif seller_user_ref.get():
        return 'Seller'
    elif admin_user_ref.get():
        return 'Admin'
    return None

#check the user status infirebase if is false or true
def check_user_status(user_role, user_id):
    user_status_ref = db.reference(user_role).child(user_id).child("status")
    return user_status_ref.get()

#check the last sign in of user
def update_last_signed_in(user_role, user_id):
    current_time = datetime.now(pytz.utc) + timedelta(hours=8)
    current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
    ref = db.reference(f"{user_role}/{user_id}")
    ref.update({"last_signed_in": current_time_str})

def generate_session_tokenadmin(user_id, user_role):
    # Generate a unique session token, for example, using a UUID
    session_token = str(uuid.uuid4())
    
    # Store the session token in Firebase under the respective user role node
    user_role_ref = db.reference(user_role).child(user_id)
    user_role_ref.update({'session_token': session_token})

# Function to delete the session token from Firebase
def delete_session_token(user_id, user_role):
    user_role_ref = db.reference(user_role).child(user_id)
    user_role_ref.child('session_token').delete()
    
# Function to get salt from Firebase
def get_user_salt(email):
    try:
        # Get the user's UID from Firebase
        user = auth.get_user_by_email(email)
        user_uid = user.uid

        # Determine the user's role (e.g., Buyer or Seller)
        user_role = determine_user_role(user_uid)

        if user_role:
        # Query the salt from the corresponding node
            user_ref = db.reference(user_role).child(user_uid)
            return user_ref.child('salt').get()

    except Exception as e:
        # Handle any errors that may occur while querying Firebase
        print(f"Error querying password salt: {str(e)}")

# Function to update forgotten password status
def update_user_forgot_status(email, status):
    try:
        # Get the user's UID from Firebase
        user = auth.get_user_by_email(email)
        user_uid = user.uid
        
        # Determine the user's role (e.g., Buyer or Seller)
        user_role = determine_user_role(user_uid)
        
        if user_role:
            # Update the status
            user_ref = db.reference(user_role).child(user_uid)
            user_ref.update({'forgot': status})
        
    except Exception as e:
        # Handle any errors that may occur while updating Firebase
        print(f"Error updating forgotten password status: {str(e)}")
        
# Function to get forgotten password status
def get_user_forgot_status(email):
    try:
        # Get the user's UID from Firebase
        user = auth.get_user_by_email(email)
        user_uid = user.uid
        
        # Determine the user's role (e.g., Buyer or Seller)
        user_role = determine_user_role(user_uid)
        
        if user_role:
            # Query the status
            user_ref = db.reference(user_role).child(user_uid)
            return user_ref.child('forgot').get()
        
    except Exception as e:
        # Handle any errors that may occur while querying Firebase
        print(f"Error querying forgotten password status: {str(e)}")