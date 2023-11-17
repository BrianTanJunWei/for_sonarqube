// AddToCartButton.js
import Cookies from 'js-cookie';
import React from 'react';
import { jwtDecode } from 'jwt-decode';

const AddToCartButton = ({ item}) => {

  let userID = '';
  const addToCart = async () => {
    try {
      // Setting Cookies up
      const cookieSession = Cookies.get('session');
      if (cookieSession){
        const sessionCookie = jwtDecode(cookieSession, { header: true });
        userID = sessionCookie.user_id;
      }
      const response = await fetch('/add-to-cart/'+userID+'/'+item.id, {
        method: 'POST',
        body: JSON.stringify({ quantity: 1 }),
        headers: {
          'Content-Type': 'application/json', // Set the content type to JSON
        },
      });

      if (response.ok) {
        // API call was successful, you can handle the response here.
        console.log('Item added to cart successfully');
        // Optionally, you can perform additional actions like updating the UI.
      } else {
        // Handle API call failure (show an error message)
        console.error('Failed to add item to cart');
      }
    } catch (error) {
      console.error('Error during API call:', error);
    }
  };
  return (
    <button onClick={addToCart}>
      Add {item.name} to Cart
    </button>
  );
};

export default AddToCartButton;
