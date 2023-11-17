from flask import request, jsonify, session, make_response
from flask_restful import Resource
from app.config.config import firebase_auth, db
from app.helpers.auth_helpers import (
    is_locked_out, set_lockout_status, increment_login_attempt,
    check_user_status, check_lockout_status
)
from app.helpers.logging_helpers import get_current_time, Login_log_to_DB
from app.helpers.verification_helpers import find_user_by_email
from datetime import datetime, timedelta
from app.shared_vars import login_attempt_counts
import pytz

# Define a route for handling login requests
class AdminLoginAPI(Resource):
    def post(self):
        try:
            # Parse the incoming JSON data from React
            login_data = request.get_json()

            # Extract the email and password from the JSON data
            email = login_data.get('email')
            password = login_data.get('password')

            # Attempt to find the user by email in Firebase
            user_found = find_user_by_email(email)
            
            if user_found is None:
                return make_response(jsonify({"success": False, "error": "No such user"}), 404)
            
            if not check_lockout_status(email):
                return make_response(jsonify({"success": False, "error": "User Account Locked. Please contact Admin"}), 401)
            
            # Check if the user has exceeded the maximum login attempts
            if user_found and is_locked_out(email):
                # Set lockout status to True
                set_lockout_status(email)
                
                # Craft a log entry and log it into the database
                log_entry = f"User {email} exceeded {login_attempt_counts[email]} Login Attempts and is locked out at {get_current_time()}"
                Login_log_to_DB(log_entry)
                return make_response(jsonify({"success": False, "error": "User locked"}), 401)
            
            # Attempt to sign in the user with email and password using Firebase Authentication
            try:
                # Sign in the user with email and password using Firebase Authentication
                user = firebase_auth.sign_in_with_email_and_password(email, password)
            except Exception as auth_error:
                # If the user was found, increment login attempt count for the user
                if user_found:
                    increment_login_attempt(email)
                    # Send logs to increment login attempt count
                    log_entry = f"User {email} Failed Login Attempt {login_attempt_counts[email]} at {get_current_time()}"
                    Login_log_to_DB(log_entry)
                
                # Handle authentication error (e.g., incorrect email or password)
                return make_response(jsonify({"success": False, "error": "Authentication failed"}), 401)

            if 'localId' in user:
                user_id = user['localId']
                
                # Check if the user is locked (status is False)
                user_status = check_user_status("Admin", user_id)

                # Check if the user exists in the "Admin" table
                admin_user_ref = db.reference('Admin').child(user_id)
                if admin_user_ref.get():
                    user_role = 'Admin'
                else:
                    return jsonify({"success": False, "error": "User not found"})

                if user_status is not None and not user_status:
                    return jsonify({"success": False, "error": "User locked"})

                # Store user session data
                session['email'] = email

                # Get the current date and time in UTC
                current_time = datetime.now(pytz.utc)
                # Add 8 hours to the current time for SG time
                current_time = current_time + timedelta(hours=8)
                # Format the new time as a string
                current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")

                # Update the "last_signed_in" attribute in the database with the formatted time
                ref = db.reference(f"{user_role}/{user_id}")
                ref.update({"last_signed_in": current_time_str})

                # Authentication was successful
                return jsonify({"success": True, "user_id": user_id, "user_role": user_role})

            else:
                # Authentication failed
                return jsonify({"success": False, "error": "Authentication failed"})

        except Exception as e:
            print('Error:', str(e))
            # Handle authentication errors and return an error response
            return jsonify({"success": False, "error": str(e)})
