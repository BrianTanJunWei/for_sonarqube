from flask import jsonify, request,make_response
from flask_restful import Resource, reqparse
from app.config.config import db, storage_ref
from datetime import timedelta
import datetime

class GetCartAPI(Resource):
    def get(self,userID):
        try:
            # Get a reference to the user's cart
            print(userID)
            cart_ref = db.reference('Cart').child(userID)
            cart = cart_ref.get()
        
            if cart:
                # Initialize an empty list to store the cart items with product information
                cart_items = []

                # Iterate through the items in the cart
                for product_id, quantity in cart.items():
                    # Retrieve product information from the "Product" table based on product_id
                    product_info = db.reference('Products').child(product_id).get()

                    if product_info:
                        # Now, retrieve the image URL for each product
                        picturepath = product_info.get('ProductPicture', '')
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
                            product_info['ProductPicture'] = url
                        # Add the product information along with the quantity to the cart_items list
                        cart_item = {
                            "product_id": product_id,
                            "quantity": quantity,
                            "productname": product_info["ProductName"],
                            "productpicture": product_info["ProductPicture"],
                            "description": product_info["description"],
                            "productcost": product_info["cost"]
                        }
                        cart_items.append(cart_item)
                    else:
                        # Handle the case where product information for a specific product_id is not found
                        return make_response(jsonify({"error": f"Product with ID {product_id} not found"}), 404)

                # Return the cart_items list containing product information as JSON with a 200 status code
                return make_response(jsonify(cart_items), 200)
            else:
                # Return a 404 status code if the cart is empty or not found
                return make_response(jsonify({"error": "Cart not found or is empty"}), 404)

        except Exception as e:
            # Return a 500 status code and the error message if an exception occurs
            return make_response(jsonify({"error": str(e)}), 500)

class AddToCartAPI(Resource):
    def post(self,userId, productId):
        try:
            if request.json is not None:
                quantity = request.json.get('quantity')
                cart_ref = db.reference(f'Cart/{userId}/{productId}')
                if quantity is None:
                    return make_response(jsonify({"error": "Quantity not provided in the request"}), 400)

                # Get current item if it exists in cart
                existing_quantity = cart_ref.get()
                if existing_quantity is not None:
                    # If item exists in cart, increase quantity
                    new_quantity = existing_quantity + quantity
                    if(new_quantity>0):
                        cart_ref.set(new_quantity)
                    else:
                        cart_ref.delete()
                    
                else:
                    # Set quantity if it doesnt exist
                    cart_ref.set(quantity)
                return make_response(jsonify({"message":"Added to cart successfully"}),200)
            else:
                return make_response(jsonify({"error": "Missing fields in request"}), 400)
        except Exception as e:
            return make_response(jsonify({"error": str(e)}))
        
class CheckoutCartAPI(Resource):
    def post(self,userId):
        try:
            cart_ref = db.reference(f'Cart/{userId}')
            user_ref = db.reference(f'Buyer/{userId}')
            user = user_ref.get()
            # Get current cart
            current_cart = cart_ref.get()
            totalCost = 0
            checkedOutProducts = {}
            if current_cart is not None:
                # Loop through items in cart
                # Get the current date and time
                current_datetime = datetime.datetime.now()
                current_time_str = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
                for key in current_cart.keys():
                    quantity = int(current_cart[key])
                    product_ref = db.reference(f'Products/{key}')
                    product = product_ref.get()
                    stock = int(product["quantity"])

                    if stock < quantity:
                        return make_response(jsonify({"error":"Quantity of "+product["ProductName"]+"not enough"}),404)
                    else:
                        totalCost = totalCost + (quantity*float(product["cost"]))
                        notification_ref = db.reference(f'Notifications/{product["sellerUID"]}')
                        new_notification_ref = notification_ref.push()
                        notif_to_add = {"product": product["ProductName"], "buyer":user["name"], "quantity": quantity, "time": current_time_str}
                        new_notification_ref.set(notif_to_add)
                        product["quantity"] = str(stock-quantity)
                        productToAdd = {"ProductName": product["ProductName"], "QuantityOrdered": quantity}
                        checkedOutProducts[key] = productToAdd
                        product_ref.set(product)


                order_ref = db.reference('Orders')
                new_order_ref = order_ref.push()
                
                order_data = {"BuyerID": userId, "Time": current_time_str, "TotalCost": round(totalCost,2), "Products":checkedOutProducts}
                new_order_ref.set(order_data)

                cart_ref.delete()

            return make_response(jsonify({"message":"Cart Checked out Successfully"}),200)
        except Exception as e:
            return make_response(jsonify({"error": str(e)}))

class DeleteFromCartAPI(Resource):
    def delete(self,userId, productId):
        try:
            cart_ref = db.reference(f'Cart/{userId}/{productId}')
            if cart_ref.get():
                # Delete the product
                cart_ref.delete()
                return make_response(jsonify({"message": f"Cart Product deleted successfully"}), 200)
            else:
                return make_response(jsonify({"message": f"No appropriate product found in cart"}), 404)
        except Exception as e:
            return make_response(jsonify({"error": str(e)}))
