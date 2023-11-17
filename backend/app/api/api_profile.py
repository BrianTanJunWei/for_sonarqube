from flask import request, jsonify, session, make_response
from flask_restful import Resource
from app.config.config import db, auth, storage_ref, client
from datetime import timedelta

class ProfileAPI(Resource):
    def get(self):
        try:
            # Check if the user is logged in and their role is in the session
            if 'user_id' in session and 'user_role' in session:
                user_id = session['user_id']
                user_role = session['user_role']
                # Fetch user details from Firebase Realtime Database
                user_ref = db.reference(user_role).child(user_id)
                user_data = user_ref.get()
                if user_data:
                    # Get user's name and age
                    name = user_data.get('name', '')
                    phonenumber = user_data.get('phonenumber', '')
                    age = user_data.get('age', '')
                    picturepath = user_data.get('profilePicture', '')
                    # Ensure that the URL contains the protocol 'https://'
                    # if not picturepath.startswith('https://'):
                    #     picturepath = 'https://' + picturepath
                    # Fetch user's email from Firebase Authentication
                    user = auth.get_user(user_id)
                    email = user.email
                    if (picturepath!=""):
                        blob = storage_ref.blob(
                            "profile_pictures/"+user_id+"/"+picturepath)
                        url = blob.generate_signed_url(
                            version="v4",
                            expiration=timedelta(minutes=15),  # Set the URL expiration time
                            method="GET",
                        )
                    else:
                        blob = storage_ref.blob(
                            "defaultpic.png")
                        url = blob.generate_signed_url(
                            version="v4",
                            expiration=timedelta(minutes=15),  # Set the URL expiration time
                            method="GET",
                        )
                    # Create a dictionary with the user's profile data
                    profile_data = {
                        'name': name,
                        'age': age,
                        'phonenumber':phonenumber,
                        'email': email,
                        'profilePicture': url  # Use the corrected URL here
                    }
                    return make_response(jsonify(profile_data), 200)
                else:
     
                    return make_response(jsonify({"error": "User data not found"}), 404)  # Return 404 when data is not found
            else:
      
                return make_response(jsonify({"error": "User not logged in"}), 404)  # Return 404 for unauthenticated users
        except Exception as e:
            return make_response(jsonify({"error": str(e)}),500)  # Return 500 for other exceptions



class UpdateProfileAPI(Resource):
    def post(self):
        try:
            # Check if the user is logged in and their role is in the session
            if 'user_id' in session and 'user_role' in session:
                user_id = session['user_id']
                user_role = session['user_role']

                # Parse the incoming form data from React
                name = request.form.get('name')
                new_phonenumber = request.form.get('phonenumber')
                profile_picture = request.files.get('profilePicture')
                # Check if phonenumber is numeric
                if not new_phonenumber.isdigit():
                    # Return an error response if the phone number is not numeric
                    response = make_response(jsonify({"error": "Phone number must be numeric"}), 400)  # HTTP 400 Bad Request
                    return response
              
                # Reference to the selected category (Buyer or Seller) in Firebase Realtime Database
                category_ref = db.reference(user_role)

                # Reference to the user's node in the selected category
                user_ref = category_ref.child(user_id)
                
                # Get the user's data from the database, including the current phone number
                user_data = user_ref.get()
                old_phonenumber = user_data.get('phonenumber')

                # Update user data in Firebase Realtime Database (name and age)
                user_ref.update({
                    'name': name,
                    'phonenumber': new_phonenumber
                })

                # Check if a new profile picture was uploaded
               # Check if a new profile picture was uploaded
                if profile_picture and profile_picture.filename.strip() != '':
                    try:
                        # Check if the file format is allowed (JPEG, PNG, JPG)
                        allowed_extensions = {'jpeg', 'jpg', 'png'}
                        file_extension = profile_picture.filename.rsplit('.', 1)[1].lower()
                        
                        if file_extension not in allowed_extensions:
                            # Return an error response if the file format is not allowed
                            response = make_response(jsonify({"error": "Invalid file format. Allowed formats: JPEG, JPG, PNG"}), 400)
                            return response

                        # Generate a unique filename for the new profile picture
                        unique_filename = f"profile_pictures/{user_id}/{profile_picture.filename}"

                        # Upload the new profile picture to Firebase Storage with the correct content type
                        blob = storage_ref.blob(unique_filename)
                        blob.upload_from_file(
                            profile_picture,
                            content_type=f"image/{file_extension}"  # Set the content type based on the file extension
                        )
                        # Update the profile picture URL in the user's database entry
                        user_ref.update({"profilePicture": profile_picture.filename})
                    except Exception as e:
                        return jsonify({"error": str(e)})
                # Compare the old and new phone numbers
                if old_phonenumber == new_phonenumber:
                    # Send SMS to the old phone number
                    client.messages.create(
                        from_='+13183024116',
                        body='Your profile has been recently updated in FerrisWheel. If this is not you, please contact the admin!',
                        to='+65' + old_phonenumber
                    )
                elif old_phonenumber != new_phonenumber:
                    client.messages.create(
                        from_='+13183024116',
                        body='Your phone number has been updated in FerrisWheel. If this is not you, please contact the admin!',
                        to='+65' + old_phonenumber
                    )
                else:
                    client.messages.create(
                        from_='+13183024116',
                        body='Your phone number has been updated as well as your personal details in FerrisWheel. If this is not you, please contact the admin!',
                        to='+65' + old_phonenumber
                    )
                 # Profile update was successful
                return make_response(jsonify({"success": True}), 200)
               
            else:
                # User not logged in (HTTP 401 Unauthorized)
                return make_response(jsonify({"error": "User not logged in"}), 401)
                
        except Exception as e:
            # Handle other exceptions (HTTP 500 Internal Server Error)
            return make_response(jsonify({"error": str(e)}), 500)
           
        
class CheckPhoneNumberExistsAPI(Resource):
    def post(self):
        try:
            # Parse the incoming JSON data from the frontend
            request_data = request.get_json()
            phone_number = request_data.get('phoneNumber')
            user_id = request_data.get('user_id')

            # Define the top-level reference to your Firebase database
            ref = db.reference()

            # Initialize the 'exists' flag
            exists = False
            # Iterate through the "Buyer" and "Seller" tables
            for table_name in ["Buyer", "Seller"]:
                table_ref = ref.child(table_name)

                # Iterate through each user in the table
                users = table_ref.get()
                if users:
                    for current_user_id, user_data in users.items():
                        if "phonenumber" in user_data and user_data["phonenumber"] == phone_number:
                            if current_user_id != user_id:
                                exists = True
                                break
            return jsonify({'exists': exists})
        except Exception as e:
            return jsonify({"error": str(e)})


