import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { verify2FA, generateSessionToken } from '../services/Services';

function TwoFactorAuthentication() {

  //pass in localstorage/cookies values for roles here 
  //can reference login.js how the session is passed then can bring it here. 
  const navigate = useNavigate();
  const [twoFA, setTwoFA] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [loggedIn, setLoggedIn] = useState(false);

  const handletwoFAChange = (e) => {
    setTwoFA(e.target.value);
  };

  const handleLogin = async (e) => {
    e.preventDefault();

    let responseData = null;

  try{
    responseData = await verify2FA(twoFA)
    if (responseData.success) {
      setLoggedIn(true);
      const tokenData = await generateSessionToken(responseData.user_id, responseData.user_role);
      const sessionToken = tokenData.session_token;

      if (responseData.user_role === 'Buyer') {
        //handle go to buyer page
        navigate('/BuyerView');
      
      }
      else if (responseData.user_role === 'Seller') {
        //handle event go to seller page
        navigate('/SellerView');
      }
      else if (responseData.user_role === 'Admin') {
        //handle event go to admin page
        navigate('/AdminView');
      }
    } else if (!responseData.success) {
      setErrorMessage(responseData.error);
    }
  } catch (error) {
    console.error('Error during 2FA authentication:', error);
    if (!responseData || !responseData.error) {
        setErrorMessage('Error during verify. Please try again.');
    }
  }
};

  return (
    <div className="container"  style={{ marginTop: "120px" }}>
      {loggedIn ? (
        <div>
          Welcome
        </div>
      ) : (
        <div>
      <h1>2FA</h1>
      <h2>Google Authentication</h2>
      {errorMessage && <div className='error-message'>{errorMessage}</div>}
      <div className="form-group d-inline">
        <label htmlFor="numberInput">Enter OTP:</label>
        <input
          type="text"
          className="form-control"
          id="numberInput"
          value={twoFA}
          onChange={handletwoFAChange}
          required
        />
      </div>
      {/* i put a handle login so on click , the proceed button will peform the functions that u stated above based on whether is seller or buyer 
        it will technically go to the buyer/seller page after 2fa is verified etc. 
      */}
      <button className="btn btn-primary" onClick={handleLogin}>Proceed</button>
      </div>
      )}
    </div>
  );
}

export default TwoFactorAuthentication;
