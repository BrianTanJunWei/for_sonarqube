def format_cost(cost):
    # Format the cost to always have two decimal places
    formatted_cost = "{:.2f}".format(float(cost))  # Convert cost to float and format it
    # Check if the formatted cost is equal to the original cost
    if formatted_cost == cost:
        # If the cost already had two decimal places, set it to the original cost
        return cost
    else:
        # If the cost did not have two decimal places, return the formatted cost
        return formatted_cost
    
def format_products(products):
    formatted_products = []

    # Iterate through products and format product details
    for product_id, product_data in products.items():
        product_name = product_data.get("ProductName", "")
        quantity_ordered = product_data.get("QuantityOrdered", "")

        formatted_products.append({
            "ProductID": product_id,
            "ProductName": product_name,
            "QuantityOrdered": quantity_ordered
        })

    return formatted_products