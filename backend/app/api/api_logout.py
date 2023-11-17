from flask import jsonify, session
from flask_restful import Resource
from app.helpers.auth_helpers import delete_session_token
from app.config.config import db, datetime,timedelta,pytz

# Define a route for handling logout requests
class LogoutAPI(Resource):
    def post(self):
        try:
            # Check if user_id is in the session, indicating the user is logged in
            if 'user_id' in session:
                user_id = session['user_id']
                user_role = session['user_role']
                
                # # Delete the session token from Firebase
                # delete_session_token(user_id, user_role)

                # Clear the user's session data 
                session.clear()
                
                # Get the current date and time in UTC
                current_time = datetime.now(pytz.utc)

                # Add 8 hours to the current time for sg time
                current_time = current_time + timedelta(hours=8)

                # Format the new time as a string
                current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")

                # Update the "last_signed_out" attribute in the database with the formatted time
                ref = db.reference(f"{user_role}/{user_id}")
                ref.update({"last_signed_out": current_time_str})

                # Return a success response
                return jsonify({"success": True})
            else:
                # If user_id is not in the session, it means the user is not logged in
                return jsonify({"success": False, "error": "User not logged in"})

        except Exception as e:
            # Handle logout errors and return an error response
            return jsonify({"success": False, "error": str(e)})