from flask import request, jsonify, session, make_response
from flask_restful import Resource
from app.helpers.auth_helpers import (
    is_locked_out, set_lockout_status, increment_login_attempt,
    determine_user_role, check_user_status, check_lockout_status,lock_user_products, get_user_forgot_status, get_user_salt
)
from app.helpers.logging_helpers import get_current_time, Login_log_to_DB
from app.helpers.verification_helpers import is_email_verified, check_concurrent_login,find_user_by_email
from app.config.config import jsonify, firebase_auth
from app.shared_vars import login_attempt_counts
import bcrypt

class LoginAPI(Resource):
    def post(self):
        try:
            # Parse the incoming JSON data from React
            login_data = request.get_json()
            email = login_data.get('email')
            password = login_data.get('password')
            role = login_data.get('userRole')

            # Attempt to find the user by email in your database
            user_found = find_user_by_email(email)

            if user_found is None:
                return make_response(jsonify({"success": False, "error": "No such user"}), 404)
            
            if not check_lockout_status(email):
                return make_response(jsonify({"success": False, "error": "User Account Locked. Please contact Admin"}), 401)

            # Check if the user has exceeded the maximum login attempts
            if user_found and is_locked_out(email):
                # Set lockout status to True
                set_lockout_status(email)

                # Lock all of user's products so buyers will not be able to see it
                if lock_user_products(email) is False:
                    print("Error! User products Not locked!")

                # Craft a log entry and log it into the database
                log_entry = f"User {email} exceeded {login_attempt_counts[email]} Login Attempts and is locked out at {get_current_time()}"
                Login_log_to_DB(log_entry)
                return make_response(jsonify({"success": False, "error": "User locked"}), 401)
            
            # Retrieving salt and Generate Hash to Authenticate
            try:
                salt = get_user_salt(email).encode('utf-8')
                hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode()
            except Exception as e:
                    return jsonify({"error": str(e)})

            # Attempt to sign in the user with email and password using Firebase Authentication
            try:
                # Get Forgotten password status
                forgot_status = get_user_forgot_status(email)
                
                if forgot_status:
                    # Attempt to reauthenticate the user with their current email and password
                    user = firebase_auth.sign_in_with_email_and_password(email, password)
                 
                else:   
                    user = firebase_auth.sign_in_with_email_and_password(email, hash)
                    
            except Exception as auth_error:
                # If the user was found, increment login attempt count for the user
                if user_found:
                    increment_login_attempt(email)
                    # Send logs to increment login attempt count
                    log_entry = f"User {email} Failed Login Attempt {login_attempt_counts[email]} at {get_current_time()}"
                    Login_log_to_DB(log_entry)

                # Handle authentication error (e.g., incorrect email or password)
                return make_response(jsonify({"success": False, "error": "Authentication failed"}), 401)

            user_id = user['localId']
            user_role = determine_user_role(user_id)
            user_status = check_user_status(user_role, user_id)

            if 'localId' not in user:
               return make_response(jsonify({"success": False, "error": "Authentication failed"}), 401)

            elif not user_role:
                return make_response(jsonify({"success": False, "error": "User Account Locked. Please contact Admin"}), 401)

            elif user_status is not None and not user_status:
                return make_response(jsonify({"success": False, "error": "User Account Locked. Please contact Admin"}), 401)

            # #for testing purposes , success set to true and error code set to 2000
            # elif not is_email_verified(user['idToken']):
            #     return make_response(jsonify({"success": True, "error": "Email is not verified. Please verify your email before logging in."}),200)
            
         #   Uncomment this for accurate return response of error 401
            elif not is_email_verified(user['idToken']):
                return make_response(jsonify({"success": False, "error": "Email is not verified. Please verify your email before logging in."}),401)
            
            # Store email in the session
            session['email'] = email

            return make_response(jsonify({"success": True, "user_id": user_id, "user_role": user_role}),200)

        except Exception as e:
            return make_response(jsonify({"success": False, "syserror": str(e)}),500)
