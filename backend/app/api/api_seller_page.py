from flask import jsonify, request,make_response
from flask_restful import Resource
from app.config.config import db, storage_ref, os, storage
from datetime import timedelta
from app.helpers.format_helpers import format_cost
import re
import imghdr

class SellerProductsAPI(Resource):
    def get(self):
        try:
            seller_uid = request.args.get('seller_uid') 
            if not seller_uid:
                return make_response(jsonify({"message": "Error! Unable to retrieve Seller UID."}), 404)
            
            products_ref = db.reference('Products')
            # Fetch all products
            products = products_ref.get()
            product_list = []
            if products:
                for product_id, product_data in products.items():
                    # Check if the SellerUID matches the provided seller_uid
                    if product_data.get('sellerUID') == seller_uid:
                        product = {
                            'ProductID': product_id,
                            'ProductName': product_data.get('ProductName', ''),
                            'quantity': product_data.get('quantity', ''),
                            'cost': product_data.get('cost', ''),
                            'description': product_data.get('description', ''),
                            'productType': product_data.get('productType', ''),
                            'status': product_data.get('status', ''),
                        }

                        # Now, retrieve the image URL for each product
                        picturepath = product_data.get('ProductPicture', '')
                        if picturepath:
                            # Construct the image URL based on seller_uid and product_id
                            image_url = f"product_pictures/{product_id}/{picturepath}"

                            # Generate a signed URL for the image
                            blob = storage_ref.blob(image_url)
                            url = blob.generate_signed_url(
                                version="v4",
                                expiration=timedelta(minutes=15),
                                method="GET",
                            )
                            product['ProductPicture'] = url

                        product_list.append(product)
        
            return make_response(jsonify(product_list),200)

        except Exception as e:
            return make_response(jsonify({"error": str(e)}),500)

class AddProductAPI(Resource):
    def post(self):
        try:
            # Extract product data fields (name, quantity, imageURL, description, productType, sellerUID)
            name = request.form.get('ProductName')
            PID = request.form.get('PID')
            quantity = request.form.get('quantity')
            cost = request.form.get('cost')
            description = request.form.get('description')
            productType = request.form.get('productType')
            sellerUID = request.form.get('sellerUID')
            availability = request.form.get('availability')
            
            # Validate product params
            if (not name or len(name) > 20) or (not quantity or float(quantity) <= 0 or (not description) or (not cost or float(cost) < 0.10)):
                return make_response(jsonify({"message": "Invalid Product Parameters! Please try again!"}), 404)
            
            # format cost to 2dp
            cost = format_cost(cost)

            # Reference to the 'Products' category in Firebase Realtime Database
            products_ref = db.reference('Products')

            # Create a new node for the product using the generated product ID
            product_ref = products_ref.child(PID)

            # Store product details in the database node
            product_ref.set({
                'ProductName': name,
                'ProductID': PID,  # Using productID as the primary key
                'quantity': quantity,
                'cost': cost,
                'description': description,
                'productType': productType,
                'sellerUID': sellerUID,  # If needed, you can still store sellerUID for reference
                'availability': availability,
                'status':True
            })
            product_picture = request.files.get('ProductPicture')
            try:
                # if product_picture and product_picture.filename.strip() != '':
                file_extension = product_picture.filename.rsplit('.', 1)[1].lower()
                                
                if file_extension not in {'png', 'jpg', 'jpeg'} or not imghdr.what(product_picture):
                    return make_response(jsonify({"message": "Invalid file format. Only .png, .jpg, and .jpeg files are allowed."}), 404)

                # Generate a unique filename for the profile picture (e.g., using a random name)
                unique_filename = f"product_pictures/{PID}/{product_picture.filename}"

                # Upload the profile picture to Firebase Storage with the correct content type
                blob = storage_ref.blob(unique_filename)
                blob.upload_from_file(
                    product_picture,
                    content_type=f"image/{file_extension}"
                )
                product_picture_url = blob.public_url

                # Add the profile picture URL to the user's database entry
                product_ref.update({"ProductPicture": product_picture.filename})

            except Exception as e:
                return make_response(jsonify({"message": "Something went wrong with uploading image. Please try again!"}), 404)

            # Product addition was successful
            return make_response(jsonify({"success": True}), 200)

        except Exception as e:
            print('Database insertion error:', str(e))
            return make_response(jsonify({"success": False, "error": str(e)}),500)


class DeleteProductAPI(Resource):
    def delete(self, productId):
        try:
            # Validate the productID using a regular expression
            if not re.match(r'^PROD\d{1,6}$', productId):
                # ProductID does not match the expected pattern
                return make_response(jsonify({"message": "Error! Invalid product"}), 404)

            # Reference to the 'Products' category in Firebase Realtime Database
            products_ref = db.reference('Products')

            # Reference to the product to delete based on productId
            product_ref = products_ref.child(productId)

            # Check if the product exists
            product_data = product_ref.get()
            if product_data:
                # Delete the product data from the Realtime Database
                product_ref.delete()
                
                # Delete the corresponding image from Firebase Storage
                if 'ProductPicture' in product_data:
                    image_url = product_data['ProductPicture']
                    if image_url:
                        # Extract the filename from the URL
                        filename = os.path.basename(image_url)
                        
                        # Reference to the product image in Firebase Storage
                        image_ref = storage.bucket().blob(f'product_pictures/{productId}/{filename}')
                        
                        # Delete the image
                        image_ref.delete()
                
                return make_response(jsonify({"message": f"Product with ID {productId} deleted successfully, including the image"}), 200)
            else:
                return make_response(jsonify({"message": f"No product found with ID {productId}"}), 404)

        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)

# Endpoint to get product by ID to populate form for edit product
class GetProductAPI(Resource):
    def get(self, productID):
        try:  
            # Validate the productID using a regular expression
            if not re.match(r'^PROD\d{1,6}$', productID):
                # ProductID does not match the expected pattern
                return make_response(jsonify({"error": "Error! Invalid product"}), 404)
            
            # Reference to the 'Products' category in Firebase Realtime Database
            products_ref = db.reference('Products')

            # Get the product under the seller's ID
            target_product_ref = products_ref.child(productID)
            product_data = target_product_ref.get()
            if product_data:
                # Return the product data as JSON with a 200 status code
                return make_response(jsonify(product_data), 200)
            else:
                # Return a 404 status code if the product is not found
                return make_response(jsonify({"error": "Product not found"}), 404)

        except Exception as e:
            # Return a 500 status code and the error message if an exception occurs
            return make_response(jsonify({"error": str(e)}), 500)

class EditProductAPI(Resource):
    def post(self, productID):
        try:
            # Validate the productID using a regular expression
            if not re.match(r'^PROD\d{1,6}$', productID):
                # ProductID does not match the expected pattern
                return make_response(jsonify({"message": "Error! Invalid product"}), 404)

            # Parse the incoming form data from React
            name = request.form.get('ProductName')
            quantity = request.form.get('quantity')
            cost = request.form.get('cost')
            ProductPicture = request.files.get('ProductPicture')  # Use 'imageFile' field to upload a new image
            description = request.form.get('description')
            productType = request.form.get('productType')
            availability = request.form.get('availability')

            # Check if any of the form fields are missing
            if any(value is None for value in (name, quantity, cost, description, productType, availability)):
                return make_response(jsonify({"error": "Missing form fields"}), 404)  
            
            # format cost to 2dp
            cost = format_cost(cost)
            
            # Reference the product you want to update
            product_ref = db.reference(f'Products/{productID}')

            # Check if the product exists
            product_data = product_ref.get()
            if product_data is None:
                return make_response(jsonify({"error": "Product not found"}), 404)  # Return a 404 Not Found status

            # Update the product information in the database
            product_ref.update({
                'ProductName': name,
                'quantity': quantity,
                'cost': cost,
                'description': description,
                'productType': productType,
                'availability': availability
            })

            # Check if a new image file was provided
            if ProductPicture and ProductPicture.filename.strip() != '':
                try:
                    # if product_picture and product_picture.filename.strip() != '':
                    file_extension = ProductPicture.filename.rsplit('.', 1)[1].lower()
                                
                    if file_extension not in {'png', 'jpg', 'jpeg'} or not imghdr.what(ProductPicture):
                        return make_response(jsonify({"message": "Invalid file format. Only .png, .jpg, and .jpeg files are allowed."}), 404)
                    
                    # Generate a unique filename for the product image (e.g., using a random name)
                    unique_filename = f"product_pictures/{productID}/{ProductPicture.filename}"

                    # Upload the new product image to Firebase Storage with the correct content type
                    blob = storage_ref.blob(unique_filename)
                    blob.upload_from_file(
                        ProductPicture,
                        content_type="image/png"  # Set the content type to PNG
                    )
                    image_url = blob.public_url

                    # Update the product's image URL in the database
                    product_ref.update({"ProductPicture": ProductPicture.filename})
                except Exception as e:
                    return make_response(jsonify({"error": str(e)}), 500)  # Return a 500 Internal Server Error status for image upload errors

            return make_response(jsonify({"message": "Product updated successfully"}), 200)  # Return a 200 OK status

        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)  # Return a 500 Internal Server Error status for other exceptions
        
class NotificationsAPI(Resource):
    def get(self):
        try:
            seller_uid = request.args.get('seller_uid')
            
            if not seller_uid:
                return make_response(jsonify({"error": "SellerID is required"}), 404)

            # Reference to the 'Notification' table in Firebase
            notifications_ref = db.reference('Notifications')

            # Get all entries under 'SellerID'
            seller_notifications = notifications_ref.child(seller_uid).get()

            if not seller_notifications:
                return make_response(jsonify([]), 200)

            #store notifications list for seller
            notifications_list = []
            # Convert the retrieved data to a list of notifications
            for notif_id, notif_data in seller_notifications.items():
                product_name = notif_data.get("product")
                buyer_email = notif_data.get("buyer")
                time = notif_data.get("time")
                quantity = notif_data.get("quantity")

                notifications_list.append({
                    "NotifID": notif_id,
                    "Product": product_name,
                    "BuyerEmail": buyer_email,
                    "Time": time,
                    "Quantity": quantity,
                })

            return make_response(jsonify(notifications_list), 200)
        
        except Exception as e:
            # Return a 500 status code and the error message if an exception occurs
            return make_response(jsonify({"error": str(e)}), 500)
        
class DeleteNotificationAPI(Resource):
    def delete(self, userId, notificationId):
        try:
            # Validate the notificationId and userId
            if not userId or not notificationId:
                return make_response(jsonify({"message": "Error! Invalid notification"}), 404)

            # Reference to the Firebase Realtime Database
            target_notification_ref = db.reference(f'Notifications/{userId}/{notificationId}')

            notification_data = target_notification_ref.get()

            if notification_data:
                # Delete the notification data from the Realtime Database
                target_notification_ref.delete()

                return make_response(jsonify({"message": f"Notification with ID {notificationId} deleted successfully"}), 200)
            else:
                return make_response(jsonify({"message": f"No notification found with ID {notificationId}"}), 404)

        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)
