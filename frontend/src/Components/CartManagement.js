
import ShoppingCart from './ShoppingCart';
import OpenCartButton from './OpenCart';
import React, { useState, useEffect } from "react";
import Cookies from 'js-cookie';
import { jwtDecode } from 'jwt-decode';

const App = () => {
  const [isCartOpen, setIsCartOpen] = useState(false);
  const [cartItems, setCartItems] = useState([]);

  let userID = '';
  // Setting Cookies up
  const cookieSession = Cookies.get('session');
  if (cookieSession){
    const sessionCookie = jwtDecode(cookieSession, { header: true });
    userID = sessionCookie.user_id;
  }

  const handleOpenCart = () => {
    setIsCartOpen(true);
    fetchCartData();
  };

  const handleCloseCart = () => {
    setIsCartOpen(false);
  };
  const handleRemoveFromCart = (itemToRemove) => {
    const updatedCart = cartItems.filter((item) => item.id !== itemToRemove.id);
    setCartItems(updatedCart);
  };
  const fetchCartData = () => {
    fetch("/get-cart/" + userID)
      .then((response) => response.json())
      .then((data) => {
        setCartItems(data);
        console.log(data);
        console.log(cartItems); // Set the fetched cart data in state
      })
      .catch((error) => {
        console.error("Error fetching cart data:", error);
      });
  };

  useEffect(() => {
    // Fetch all products from the Flask backend when the component mounts
    fetchCartData();
  }, []);

  return (
    <div>
      <OpenCartButton onClick={handleOpenCart} />
      <ShoppingCart
        isOpen={isCartOpen}
        onClose={handleCloseCart}
        cartItems={cartItems}
        onRemoveFromCart={handleRemoveFromCart}
        fetchCartData={fetchCartData}
      />
    </div>
    
  );
};

export default App;
