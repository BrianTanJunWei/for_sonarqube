from flask import jsonify, make_response
from flask_restful import Resource, reqparse
from app.config.config import db, storage_ref
from datetime import timedelta

# Create a route to fetch all products
class FetchAllProductsAPI(Resource):
    def get(self):
        try:
            # Reference to the 'Products' category in Firebase Realtime Database
            products_ref = db.reference('Products')

            # Fetch all products
            products = products_ref.get()

            # Convert the products data to a list
            product_list = []
            if products:
                for product_id, product_data in products.items():
                    # Check the 'status' attribute, and skip if it's false
                    if product_data.get('status', True):
                        product = {
                            'ProductID': product_id,
                            'ProductName': product_data.get('ProductName', ''),
                            'quantity': product_data.get('quantity', ''),
                            'cost': product_data.get('cost', ''),
                            'description': product_data.get('description', ''),
                            'productType': product_data.get('productType', ''),
                            'availability': product_data.get('availability', ''),
                        }
                        # Now, retrieve the image URL for each product
                        picturepath = product_data.get('ProductPicture', '')
                        if picturepath:
                            # Construct the image URL for the product
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
        
# Create a route to fetch filtered products
class FetchFilteredProductsAPI(Resource):
    def get(self, producttype):
        try:
            # Reference to the 'Products' category in Firebase Realtime Database
            products_ref = db.reference('Products')

            # Fetch all products
            products = products_ref.get()

            # Convert the products data to a list
            product_list = []
            if products:
                for product_id, product_data in products.items():
                    if product_data.get('productType', '') == producttype:
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
                            # Construct the image URL for the product
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

            if(len(product_list)==0):
                return make_response(jsonify(product_list),404)
            else:
                return jsonify(product_list)
        except Exception as e:
            return jsonify({"error": str(e)})