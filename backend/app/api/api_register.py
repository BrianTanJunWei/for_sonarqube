from flask import request, jsonify, session, make_response
from flask_restful import Resource
from app.config.config import db, storage_ref,firebase_auth
from datetime import timedelta
from firebase_admin import auth
from app.helpers.verification_helpers import(find_user_by_email, check_phone_number_exists,check_name_exists)
from werkzeug.utils import secure_filename
from app.config.config import(storage_ref)
import pyotp, bcrypt

# Define the allowed file extensions
allowed_extensions = {'jpg', 'jpeg', 'png'}
class RegisterAPI(Resource):
    def post(self):
        try:
            # Parse the incoming form data from React
            name = request.form.get('name')
            phonenumber = request.form.get('phoneNumber')
            age = request.form.get('age')
            email = request.form.get('email')
            password = request.form.get('password')
            role = request.form.get('role')
            profile_picture = request.files.get('profilePicture')
            # Generate Salt and Hashing password
            salt = bcrypt.gensalt(15)
            hash = bcrypt.hashpw(password.encode('utf-8'), salt)
            
             # Check if phonenumber and age are valid numbers
            print(profile_picture)
            try:
                phonenumber = int(phonenumber)
                age = int(age)
                
            except ValueError:
                return make_response(jsonify({"success": False, "error": "Phone number and age must be valid numbers"}), 400)
              # Check file extension for profile picture

            # Check file extension for profile picture if it's not empty
            if profile_picture and len(profile_picture.getbuffer()) > 0:
                filename = secure_filename(profile_picture.filename)
                if '.' in filename and filename.rsplit('.', 1)[1].lower() not in {'jpg', 'jpeg', 'png'}:
                 return make_response(jsonify({"success": False, "error": "Invalid file format. Allowed formats: .jpg, .jpeg, .png"}), 400)
                 
            email_exists = find_user_by_email(email)
            phone_number_exists = check_phone_number_exists(phonenumber,role)
            name_exists = check_name_exists(name,role)

            if email_exists:
                return make_response(jsonify({"success": False, "error": "Email already exists"}), 400)
            # Register the user with Firebase Authentication
                
            if phone_number_exists:
                return make_response(jsonify({"success": False, "error": "Phone number already exists"}), 400)
            
            if name_exists:
                return make_response(jsonify({"success": False, "error": "Name already exists"}), 400)
            
            # Decoding hashed password and salt from bytes object to string
            try:
                hashed = hash.decode()
                salted = salt.decode()
            except Exception as e:
                    return jsonify({"error": str(e)})
            
            user = firebase_auth.create_user_with_email_and_password(email, hashed)
    
            # Get the UID of the newly created user
            user_id = user['localId']
            
            firebase_auth.send_email_verification(user['idToken'])
            # Determine the database node (Buyer or Seller) based on user's selection
            if role == 'Seller':
                database_node = 'Seller'
            elif role == 'Buyer':
                database_node = 'Buyer'
            else:
                return make_response(jsonify({"success": False, "error": "Invalid role selection"}), 400)

            # Reference to the selected category (Buyer or Seller) in Firebase Realtime Database
            category_ref = db.reference(database_node)

            # Create a new node using the UID as the key and store user details
            user_ref = category_ref.child(user_id)
            
            # Generate TOTP for QR Code
            secretTOTP = pyotp.random_base32()
            uri = pyotp.totp.TOTP(secretTOTP).provisioning_uri(name=email, issuer_name="FerrisWheel")
            session['uri'] = uri
            
            # Store user details in the database node
            user_ref.set({
                'name': name,
                'age': age,
                'phonenumber':phonenumber,
                'secret': secretTOTP,
                'uri': uri,
                'salt': salted,
                'forgot': False,
                'status': True # default status is true when account is created
            })
            
            profile_picture = request.files.get('profilePicture')
        # Check if a file was uploaded (profile_picture is not None) and if it's not an empty file
            if profile_picture and profile_picture.filename.strip() != '':
                try:
                    # Generate a unique filename for the profile picture (e.g., using a random name)
                    import uuid
                    unique_filename = f"profile_pictures/{user_id}/{profile_picture.filename}"

                    # Upload the profile picture to Firebase Storage with the correct content type
                    blob = storage_ref.blob(unique_filename)
                    blob.upload_from_file(
                        profile_picture,
                        content_type="image/png"  # Set the content type to PNG
                    )
                    profile_picture_url = blob.public_url

                    # Add the profile picture URL to the user's database entry
                    user_ref.update({"profilePicture": profile_picture.filename})

                except Exception as e:
                    return jsonify({"error": str(e)})
        
            # Registration was successful
            return make_response(jsonify({"success": True}), 200)
        
        except Exception as e:
            print('Error during registration:', str(e))
            return make_response(jsonify({"success": False, "error": str(e)}),500) 
 

class DeleteUserAPI(Resource):
    def post(self):
        try:
            # Get the user's email from the request
            email = request.form.get('email')

            # Find the user by email and get the UID
            user = auth.get_user_by_email(email)
            user_id = user.uid

            # Check if the user exists in the Seller node in the Realtime Database
            seller_ref = db.reference('/Seller')
            seller_user = seller_ref.child(user_id).get()

            # Check if the user exists in the Buyer node in the Realtime Database
            buyer_ref = db.reference('/Buyer')
            buyer_user = buyer_ref.child(user_id).get()

            if seller_user is not None:
                # User exists in the Seller node, delete from there
                seller_ref.child(user_id).delete()

            if buyer_user is not None:
                # User exists in the Buyer node, delete from there
                buyer_ref.child(user_id).delete()

            # Delete the user from Firebase Authentication
            auth.delete_user(user_id)

            # Determine the file path for the profile picture
            profile_picture_path = f'/profile_pictures/{user_id}'  # Adjust this path as needed
            
            # Delete the profile picture from Google Cloud Storage
            blob = storage_ref.blob(profile_picture_path)
            if blob.exists():
                blob.delete()

            return jsonify({"success": True})
        
        except Exception as e:
            return jsonify({"success": False, "error": str(e)})