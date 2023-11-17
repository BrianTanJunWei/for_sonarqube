
import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import '../css/ShoppingCart.css';
import Cookies from 'js-cookie';
import { jwtDecode } from 'jwt-decode';

const ShoppingCart = ({ isOpen, onClose, cartItems, fetchCartData}) => {
    console.log(cartItems)
      // Call fetchCartData whenever you need to update the cart data
    const updateCartData = () => {
      fetchCartData();
    };

    let userID = '';
    // Setting Cookies up
    const cookieSession = Cookies.get('session');
    if (cookieSession){
      const sessionCookie = jwtDecode(cookieSession, { header: true });
      userID = sessionCookie.user_id;
    }

    const removeFromCart = async (item) => {
      try {
        // Setting Cookies up
        // const cookieSession = Cookies.get('session');
        // if (cookieSession){
        //   const sessionCookie = jwtDecode(cookieSession, { header: true });
        //   userID = sessionCookie.user_id;
        // }
        const response = await fetch('/delete-from-cart/'+userID+'/'+item.product_id, {
          method: 'DELETE',
        });
  
        if (response.ok) {
          // API call was successful, you can handle the response here.
          console.log('Item deleted successfully');
          updateCartData()
          // Optionally, you can perform additional actions like updating the UI.
        } else {
          // Handle API call failure (show an error message)
          console.error('Failed to delete item from cart');
        }
      } catch (error) {
        console.error('Error during API call:', error);
      }
    };
    const onIncreaseQuantity = async (item) => {
      try {
        // Setting Cookies up
        // const cookieSession = Cookies.get('session');
        // if (cookieSession){
        //   const sessionCookie = jwtDecode(cookieSession, { header: true });
        //   userID = sessionCookie.user_id;
        // }
        const response = await fetch('/add-to-cart/'+userID+'/'+item.product_id, {
          method: 'POST',
          body: JSON.stringify({ quantity: 1 }),
          headers: {
            'Content-Type': 'application/json', // Set the content type to JSON
          },
        });
        if (response.ok) {
          // API call was successful, you can handle the response here.
          console.log('Item increased successfully');
          updateCartData()
          // Optionally, you can perform additional actions like updating the UI.
        } else {
          // Handle API call failure (show an error message)
          console.error('Failed to increase item in cart');
        }
      } catch (error) {
        console.error('Error during API call:', error);
      }
    };
    const onDecreaseQuantity = async (item) => {
      try {
        // Setting Cookies up
        // const cookieSession = Cookies.get('session');
        // if (cookieSession){
        //   const sessionCookie = jwtDecode(cookieSession, { header: true });
        //   userID = sessionCookie.user_id;
        // }
        const response = await fetch('/add-to-cart/'+userID+'/'+item.product_id, {
          method: 'POST',
          body: JSON.stringify({ quantity: -1 }),
          headers: {
            'Content-Type': 'application/json', // Set the content type to JSON
          },
        });
  
        if (response.ok) {
          // API call was successful, you can handle the response here.
          console.log('Item deleted successfully');
          updateCartData()
          // Optionally, you can perform additional actions like updating the UI.
        } else {
          // Handle API call failure (show an error message)
          console.error('Failed to delete item from cart');
        }
      } catch (error) {
        console.error('Error during API call:', error);
      }
    };
  return (
    isOpen && (
      <div className="shopping-cart">
        <button className="close-button" onClick={onClose}>
          &times;
        </button>
        <h2>Your Shopping Cart</h2>
        {cartItems.error ? (
          <p>Your cart is empty.</p>
        ) : (
          <div>
            {cartItems.map((item) => (
              <div className="cart-item" key={item.product_id}>
                <div className="product-image">
                  <img src={item.productpicture} alt={item.name} />
                </div>
                <div className="product-info">
                <div className="product-details">
                    <h3>{item.productname}</h3>
                    <p>Cost: ${item.productcost}</p>
                  </div>
                <div className="quantity-control">
                  <button onClick={() => onDecreaseQuantity(item)} class="btn btn-light">
                    -
                  </button>
                  <span>{item.quantity}</span>
                  <button onClick={() => onIncreaseQuantity(item)} class="btn btn-light">
                   +
                  </button>
                </div>
                <button className="remove-button" onClick={() => removeFromCart(item)} class="btn btn-light">Remove</button>
              </div>
              </div>
            ))}
            
            <Link to="/Checkout">
              <button class="btn btn-dark">
                Checkout
              </button>
            </Link>
              
          </div>
        )}
        
      </div>
    )
  );
};

export default ShoppingCart;
