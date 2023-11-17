import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import LoginForm from '../Components/LoginForm';
import { login, generateSessionToken, verifyCaptcha } from '../services/Services'; // Import the service functions
import "../css/login.css";
import ReCAPTCHA from 'react-google-recaptcha';
import Cookies from 'js-cookie';
import { jwtDecode } from "jwt-decode";

function Login() {
  // Initialize state based on Cookies when component mounts
  useEffect(() => {
    const cookieSession = Cookies.get('session');
    let storedUserId = '';
    let storedUserRole = '';
    let storedUserName = '';
    // Check if Cookie is undefined
    if (cookieSession) {
      if (cookieSession.charAt(0) === 'e'){
        const sessionCookie = jwtDecode(cookieSession, { header: true });
        storedUserId = sessionCookie.user_id;
        storedUserRole = sessionCookie.user_role;
        storedUserName = Cookies.get('user_name');
        // storedtoken =   sessionCookie.session_token; Not being used
      }
    }
      if (storedUserId && storedUserRole && storedUserName) {
        setLoggedIn(true);
        setUserName(storedUserName);
        setUserRole(storedUserRole);
      } else {
        // Set default values when there is no data in Cookies
        setEmail('');
        setPassword('');
        setLoggedIn(false);
        setUserName('');
        setUserRole('');
      }
  }, []); // Empty dependency array ensures this effect runs once when component mounts

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loggedIn, setLoggedIn] = useState(false);
  const [userName, setUserName] = useState('');

  const [userRole, setUserRole] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const navigate = useNavigate();
  const [recaptchaResponse, setRecaptchaResponse] = useState(''); // For reCAPTCHA

  const handleEmailChange = (e) => {
    setEmail(e.target.value);
  };

  const handlePasswordChange = (e) => {
    setPassword(e.target.value);
  };

  const handleRecaptchaChange = (token) => {
    setRecaptchaResponse(token); // Store the reCAPTCHA token
  }

  const handleLogin = async (role, e) => {
    e.preventDefault();

  let responseData = null; // Define responseData with an initial value
  let response = null;

  try {
    response = await verifyCaptcha(recaptchaResponse); // reCAPTCHA verification
    responseData = await login(email, password);
  
    if (response && responseData.success && responseData.user_role === role) {
      // setLoggedIn(true);
      setUserName(responseData.user_name);
      setUserRole(responseData.user_role);
      
      Cookies.set('user_name', responseData.user_name);
      if (role === 'Buyer' || role === 'Seller') {
        navigate('/TwoFactorAuthentication');
      } else {
        console.error('Login failed');
      }
    } else if (!responseData.success) {
      setErrorMessage(responseData.error);
    }
  } catch (error) {
  console.error('Error during login:', error);
    if (!responseData || !responseData.error) {
        setErrorMessage('Error during login. Please try again.');
    }
  }
  
  };
  return (
    <div className="login-container">
      {loggedIn ? (
        <div>
          Welcome, {userName}
        </div>
      ) : (
        <div className="login-form">
          <h2>Login</h2>
          {errorMessage && <div className="error-message">{errorMessage}</div>}
          <LoginForm
        email={email}
        password={password}
        handleEmailChange={handleEmailChange}
        handlePasswordChange={handlePasswordChange}
        handleLogin={handleLogin}
        role={userRole} // Pass the userRole to the LoginForm.
            />
            <ReCAPTCHA
              sitekey="6Lf0zcsoAAAAAItrGtc2tjuTnu8rt3BBojtI9nr5"
              onChange={handleRecaptchaChange}
            />
            <div>
              <Link to="/CreateAccount">Create Account</Link>
            </div>
            <div>
              <Link to="/ForgetPassword">Forget Password</Link>
            </div>
         
        </div>
      )}
    </div>
  );
}

export default Login;