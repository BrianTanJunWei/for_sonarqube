from flask import jsonify,request, make_response
from flask_restful import Resource
from app.config.config import auth, db
from app.helpers.auth_helpers import reset_login_attempt,unlock_user_products
from app.helpers.format_helpers import format_products

class GetAccountsAPI(Resource):
    def get(self):
        try:
            # Fetch user records from Firebase Authentication
            users = auth.list_users()
            user_data=[]
            for user in users.iterate_all():
                user_info = {
                    "identifier": user.email,
                    "role": None,
                    "last_signed_in": None,
                    "last_signed_out": None,
                    "status": False, 
                }

                # Check Buyer table for user
                buyer_ref = db.reference(f"Buyer/{user.uid}")
                buyer_data = buyer_ref.get()

                if buyer_data:
                    user_info["role"] = "Buyer"
                    user_info["last_signed_in"] = buyer_data.get("last_signed_in")
                    user_info["last_signed_out"] = buyer_data.get("last_signed_out")
                    user_info["status"] = buyer_data.get("status", False)  # Update status if present

                # Check Seller table for user
                seller_ref = db.reference(f"Seller/{user.uid}")
                seller_data = seller_ref.get()

                if seller_data:
                    user_info["role"] = "Seller"
                    user_info["last_signed_in"] = seller_data.get("last_signed_in")
                    user_info["last_signed_out"] = seller_data.get("last_signed_out")
                    user_info["status"] = seller_data.get("status", False)  # Update status if present

                # Check Admin table for user
                admin_ref = db.reference(f"Admin/{user.uid}")
                admin_data = admin_ref.get()

                if admin_data:
                    user_info["role"] = "Admin"
                    user_info["last_signed_in"] = admin_data.get("last_signed_in")
                    user_info["last_signed_out"] = admin_data.get("last_signed_out")
                    user_info["status"] = admin_data.get("status", False)  # Update status if present
                user_data.append(user_info)

            return make_response(jsonify(user_data),200)

        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)

class UpdateUserStatusAPI(Resource):
    def post(self):
        try:
            data = request.get_json()
            user_id = data.get("userId")
            user_role = data.get("role")
            disabled = data.get("disabled")

            if any(value is None for value in (user_id, user_role, disabled)):
                return make_response(jsonify({"error": "Missing fields. Please try again"}), 404)

            try:
                # Use Firebase Admin SDK to get user information by email
                user = auth.get_user_by_email(user_id)
                # Access user.email to get the user's email
                email = user.email
                # Access user.uid to get the Firebase UID
                uid = user.uid

                user_ref = db.reference(f"{user_role}/{uid}")
                user_ref.update({"status": disabled})

                # Reset counter to 0 when status is set to true.
                reset_login_attempt(email)

                #Unlock User Products so buyers will be able to see them
                if unlock_user_products(email) is False:
                    print("Error! Something went wrong! User products not unlocked!")

                # Check if a session token exists and delete it if found in case the user is currently logged in
                session_token_ref = db.reference(f"{user_role}/{uid}/session_token")
                session_token = session_token_ref.get()
                if session_token:
                    session_token_ref.delete()
                    try:
                        auth.revoke_refresh_tokens(uid)

                        # Log out the user by reauthenticating with an empty custom token
                        empty_custom_token = auth.create_custom_token(uid, {})
                        auth.sign_in_with_custom_token(empty_custom_token)
                    except Exception as token_error:
                        # Handle token revocation error
                        print(f"Error revoking tokens: {str(token_error)}")

                return make_response(jsonify({"success": True}), 200)
            except Exception as user_error:
                # Handle exceptions related to user retrieval and updates
                return make_response(jsonify({"error": "User does not exist!"}), 404)

        except Exception as e:
            # Handle other exceptions
            return make_response(jsonify({"error": str(e)}), 500)
        
# Define a route to fetch login logs data
class LoginLogsAPI(Resource):
    def get(self):
        try:
            # Reference to the 'Login_Logs' table in Firebase
            login_logs_ref = db.reference('Login_logs')

            # Get all entries under 'Login_Logs'
            entries = login_logs_ref.get()
            #store logs
            login_logs = []
            # Loop through the entries and append them to the login_logs list
            for key, entry in entries.items():
                login_logs.append({"key": key, "entry": entry})
            # Show latest logs at the top
            login_logs.reverse()
            return make_response(jsonify(login_logs),200)

        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)
        
class TransactionLogsAPI(Resource):
    def get(self):
        try:
            # Reference to the 'Orders' table in Firebase
            orders_ref = db.reference('Orders')

            # Get all entries under 'Orders'
            entries = orders_ref.get()
            transaction_logs = []
            # Loop through the entries and append them to the transaction_logs list
            for order_id, order_data in entries.items():
                buyer_id = order_data.get("BuyerID", "")
                time = order_data.get("Time", "")
                total_cost = order_data.get("TotalCost", "")
                products = format_products(order_data.get("Products", {}))

                transaction_logs.append({
                    "OrderID": order_id,
                    "BuyerID": buyer_id,
                    "Time": time,
                    "TotalCost": total_cost,
                    "Products": products
                })

            # Show latest logs at the top
            transaction_logs.reverse()

            return make_response(jsonify(transaction_logs),200)

        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)

    