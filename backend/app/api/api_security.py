from flask import request, jsonify, session, make_response
from flask_restful import Resource
from app.config.config import firebase_auth, db,uuid,auth, captchaSecret
from app.helpers.auth_helpers import getCurrentSessionToken, reset_login_attempt, update_last_signed_in, determine_user_role, update_user_forgot_status, get_user_forgot_status, get_user_salt
from app.helpers.logging_helpers import get_current_time, Login_log_to_DB
import re, requests, pyotp, bcrypt

class GetCurrentSessionTokenAPI(Resource):
    def post(self):
        data = request.get_json()
        session_token = data.get('session_token')
        user_id = data.get('user_id')
        user_role = data.get('user_role')
        sestoken  = getCurrentSessionToken(user_id , user_role)
        if session_token == sestoken:
            return jsonify({"valid": True})
        else:
            session.clear() # Clear cookies and session
            return jsonify({"valid": False})  # Unauthorized status code
    
class GenerateSessionTokenAPI(Resource):
    def post(self):
        try:
            user_id = request.json.get('user_id')
            user_role = request.json.get('user_role')
            # Generate a unique session token, for example, using a UUID
            session_token = str(uuid.uuid4())
             # Store the session token in the session
            session['session_token'] = session_token
            # Store the session token in Firebase under the respective user role node
            user_role_ref = db.reference(user_role).child(user_id)
            user_role_ref.update({'session_token': session_token})
           
            return jsonify({"success": True, "session_token": session_token})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)})

class ForgotPasswordAPI(Resource):
    def post(self):
        try:
            # Parse the incoming JSON data from React
            data = request.get_json()

            # Extract the email address from the JSON data
            email = data.get('email')
                        
            # Check if the email is in a valid format
            email_regex = r"^[^\s@]+@[^\s@]+.[^\s@]+"
            if not re.match(email_regex, email):
                # Return an error response if the email is not in a valid format
                return make_response(jsonify({"success": False, "error": "Invalid email format"}),404)

            # Send a password reset email using Firebase Authentication
            firebase_auth.send_password_reset_email(email)
            
            # Update forgotten password status
            update_user_forgot_status(email, True)
            
            # Return a success response
            return make_response(jsonify({"success": True, "message": "Password reset email sent. Check your inbox."}),200)

        except Exception as e:
            # Handle other errors and return an error response
            return make_response(jsonify({"success": False, "error": str(e)}),404)
        
class ChangePasswordAPI(Resource):
    def post(self):
        try:
            if 'user_id' in session and 'user_role' in session:
                user_id = session['user_id']
                user_role = session['user_role']

                # Get the JSON data from the request
                data = request.get_json()
                                
                # Extract the currentPassword and newPassword from the data
                current_password = data.get('currentPassword')
                new_password = data.get('newPassword')

                # Reauthenticate the user
                user = auth.get_user(user_id)
                user_email = user.email
                
                # Retrieving salt and Generate Hash to authenticate
                try:
                    salt = get_user_salt(user_email).encode('utf-8')
                    hash = bcrypt.hashpw(current_password.encode('utf-8'), salt).decode()
                except Exception as e:
                    return jsonify({"error" : str(e)})
                                    
                # Salt and hash the new password
                new_hash = bcrypt.hashpw(new_password.encode('utf-8'), salt).decode()

                try:
                    # Get Forgotten password status
                    forgot_status = get_user_forgot_status(user_email)
                    
                    if forgot_status:
                        # Attempt to reauthenticate the user with their current email and password
                        firebase_auth.sign_in_with_email_and_password(user_email, current_password)
                        
                        # If reauthentication is successful, change the password
                        auth.update_user(
                            user_id,
                            password=new_hash
                        )
                                                
                        # Update forgotten password status
                        update_user_forgot_status(user_email, False)
                        
                    else:
                        # Attempt to reauthenticate the user with their current email and password
                        firebase_auth.sign_in_with_email_and_password(user_email, hash)
                        
                        # If reauthentication is successful, change the password
                        auth.update_user(
                            user_id,
                            password=new_hash
                        )

                    return make_response(jsonify({'message': 'Password changed successfully'}), 200)
                
                except auth.AuthError as e:
                    # If reauthentication fails, return an error response
                    return  make_response(jsonify({'error': f'Failed to reauthenticate: {str(e)}'}), 401)

                except Exception as e:
                    # Handle other errors and return an error response
                    return make_response(jsonify({'error': str(e)}), 500)

            else:
                # Handle the case where the user is not authenticated
                return make_response(jsonify({'error': 'User not authenticated'}), 401)

        except Exception as e:
            # Handle other errors and return an error response
           return make_response(jsonify({'error': str(e)}), 500)
       
class VerifyCaptchaAPI(Resource):
    def post(self):
        try:
            data = request.get_json()
            recaptcha_response = data.get('recaptchaResponse')
            secret_key = captchaSecret
            
            # Verify the reCAPTCHA response
            verification_url = f'https://www.google.com/recaptcha/api/siteverify?secret={secret_key}&response={recaptcha_response}'
            response = requests.post(verification_url)
            verification_data = response.json()
            
            if verification_data['success']:
                # reCAPTCHA Verification Successful
                return make_response(jsonify({"success": True}), 200)
                
            else:
                # reCAPTCHA Verification Failed
                return make_response(jsonify({"error": "reCAPTCHA verification failed"}) , 401)
            
        except Exception as e:
            # Handle exceptions and return a JSON response
            error_messsage = str(e)
            return make_response(jsonify({"error": error_messsage}), 400)
        
class GetUriAPI(Resource):
    def get(self):
        try:
            # Get the URI from Session created from register
            uri = session.get('uri')
            if uri is not None:
                session.pop('uri', None)
                return make_response(jsonify({"uri": uri}), 200)
            else:
                return make_response(jsonify({"error": "URI not found in session"}), 404)
        
        except Exception as e:
            # Handle exceptions and return a JSON response
            error_message = str(e)
            return make_response(jsonify({"error": error_message}), 500)
        
class Verify2FAAPI(Resource):
    def post(self):
        try:
            # Get 2FA code from React
            data = request.get_json()
            twoFA = data.get('twoFA')
            
            # Get email from session
            email = session.get('email')
            if email is None:
                return make_response(jsonify({"error": "Email not found in session"}), 404)
            
            # Get usér's UID from Firebase
            user = auth.get_user_by_email(email)
            user_uid = user.uid
            
            # Determine the user's role (e.g., Buyer or Seller)
            user_role = determine_user_role(user_uid)
            
            # Query secret from Firebase
            user_ref = db.reference(user_role).child(user_uid)
            secret = user_ref.child('secret').get()
            
            # Verify 2FA OTP
            totp = pyotp.TOTP(secret)
            if totp.verify(twoFA):
                # Store user information in the session
                session.pop('email', None)
                session['user_id'] = user_uid
                session['user_role'] = user_role

                update_last_signed_in(user_role, user_uid)
                # Reset login attempt count for the user upon successful login
                reset_login_attempt(email)
                # Craft a log entry and log it into the database
                log_entry = f"User {email} has logged in at {get_current_time()}"
                Login_log_to_DB(log_entry)
                return make_response(jsonify({"success": True, "user_id": user_uid, "user_role": user_role}), 200)
            else:
                return make_response(jsonify({"error" : "OTP does not match"}), 401)
            
        except Exception as e:
            # Handle exceptions and return a JSON response
            error_message = str(e)
            return make_response(jsonify({"error": error_message}), 500)   