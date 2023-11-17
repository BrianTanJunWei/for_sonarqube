import React, { useState, useEffect } from 'react';
import Cookies from 'js-cookie';
import { jwtDecode } from 'jwt-decode';

const Checkout = () => {
  const [cartItems, setCartItems] = useState([]);

  let userID = '';
  // Setting Cookies up
  const cookieSession = Cookies.get('session');
  if (cookieSession) {
    const sessionCookie = jwtDecode(cookieSession, { header: true });
    userID = sessionCookie.user_id;
  }

  const [formData, setFormData] = useState({
    cardNumber: '',
    expirationDate: '',
    cvv: '',
  });
  const [errors, setErrors] = useState({});
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };
  const validate = () => {
    const newErrors = {};
    // Validate card number (you can customize this validation)
    if (!formData.cardNumber.match(/^\d{16}$/)) {
      newErrors.cardNumber = 'Invalid card number';
    }

    // Validate expiration date (you can customize this validation)
    if (!formData.expirationDate.match(/^\d{2}\/\d{2}$/)) {
      newErrors.expirationDate = 'Invalid expiration date';
    }

    // Validate CVV (you can customize this validation)
    if (!formData.cvv.match(/^\d{3}$/)) {
      newErrors.cvv = 'Invalid CVV';
    }

    setErrors(newErrors);

    return Object.keys(newErrors).length === 0;
  };
  const handleSubmit = (e) => {
    e.preventDefault();

    const isValid = validate();
    
    if (isValid) {
      // Form is valid, you can proceed with submitting the payment
      // For example, you can make an API request to process the payment here
      console.log('Form data is valid:', formData);
    } else {
      // Form is invalid, do not submit
      console.log('Form data is invalid');
    }
  };
  useEffect(() => {
    // Fetch cart data when the component mounts
    fetchCartData();
  }, []); // An empty dependency array ensures that it runs only once when the component mounts

  function fetchCartData() {
    fetch("/get-cart/" + userID)
      .then((response) => response.json())
      .then((data) => {
        setCartItems(data);
        console.log(data);
      })
      .catch((error) => {
        console.error("Error fetching cart data:", error);
      });
  }
  const removeFromCart = async (item) => {
    try {
      const cookieSession = Cookies.get('session');
      if (cookieSession) {
        const sessionCookie = jwtDecode(cookieSession, { header: true });
        userID = sessionCookie.user_id;
      }
      const response = await fetch('/delete-from-cart/'+userID+'/'+item.product_id, {
        method: 'DELETE',
      });

      if (response.ok) {
        // API call was successful, you can handle the response here.
        console.log('Item deleted successfully');
        fetchCartData()
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
      const cookieSession = Cookies.get('session');
      if (cookieSession) {
        const sessionCookie = jwtDecode(cookieSession, { header: true });
        userID = sessionCookie.user_id;
      }
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
        fetchCartData()
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
      const cookieSession = Cookies.get('session');
      if (cookieSession) {
        const sessionCookie = jwtDecode(cookieSession, { header: true });
        userID = sessionCookie.user_id;
      }
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
        fetchCartData()
        // Optionally, you can perform additional actions like updating the UI.
      } else {
        // Handle API call failure (show an error message)
        console.error('Failed to delete item from cart');
      }
    } catch (error) {
      console.error('Error during API call:', error);
    }
  };
  const CheckoutCartData = async (item) => {
    try {
      const cookieSession = Cookies.get('session');
      if (cookieSession) {
        const sessionCookie = jwtDecode(cookieSession, { header: true });
        userID = sessionCookie.user_id;
      }
      const response = await fetch('/checkout/'+userID, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json', // Set the content type to JSON
        },
      });

      if (response.ok) {
        // API call was successful, you can handle the response here.
        console.log('Item deleted successfully');
        // Optionally, you can perform additional actions like updating the UI.
      } else {
        // Handle API call failure (show an error message)
        console.error('Failed to delete item from cart');
      }
    } catch (error) {
      console.error('Error during API call:', error);
    }
    fetchCartData()
  };

  return (
    <div className="container mt-5">
      <h2 className="text-center">Checkout</h2>
      {cartItems.error ? (
        <p>Your cart is empty. Please add products into your cart before checking out.</p>
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
                  <p>Description: {item.description}</p>
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
                <button className="remove-button" onClick={() => removeFromCart(item)} class="btn btn-light">
                  Remove
                </button>
              </div>
            </div>
          ))}
          <div>
            <h2>Payment Information</h2>
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label htmlFor="cardNumber">Card Number</label>
                <input
                  type="text"
                  name="cardNumber"
                  className={`form-control ${errors.cardNumber ? 'is-invalid' : ''}`}
                  value={formData.cardNumber}
                  onChange={handleChange}
                />
                {errors.cardNumber && (
                  <div className="invalid-feedback small">{errors.cardNumber}</div>
                )}
              </div>
              <div className="form-group">
                <label htmlFor="expirationDate">Expiration Date</label>
                <input
                  type="text"
                  name="expirationDate"
                  className={`form-control ${errors.expirationDate ? 'is-invalid' : ''}`}
                  value={formData.expirationDate}
                  onChange={handleChange}
                />
                {errors.expirationDate && (
                  <div className="invalid-feedback small">{errors.expirationDate}</div>
                )}
              </div>
              <div className="form-group">
                <label htmlFor="cvv">CVV</label>
                <input
                  type="text"
                  name="cvv"
                  className={`form-control ${errors.cvv ? 'is-invalid' : ''}`}
                  value={formData.cvv}
                  onChange={handleChange}
                />
                {errors.cvv && (
                  <div className="invalid-feedback small">{errors.cvv}</div>
                )}
              </div>
            </form>
            <button className="btn btn-primary" onClick={CheckoutCartData}>
                Submit Payment
              </button>
          </div>
        </div>
        
      )}
      
    </div>
  );
} 

export default Checkout;
