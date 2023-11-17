// pages/AdminLogin.js
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import LoginForm from '../Components/LoginForm';
import {adminLogin, verifyCaptcha} from '../services/Services';
import ReCAPTCHA from 'react-google-recaptcha';
import Cookies from 'js-cookie';
import { jwtDecode } from 'jwt-decode';

const AdminLogin = () => {
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
    }, []);

    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [loggedIn, setLoggedIn] = useState(false);
    const [userName, setUserName] = useState('');
    const [userRole, setUserRole] = useState('');
    const [errorMessage, setErrorMessage] = useState('');
    const [recaptchaResponse, setRecaptchaResponse] = useState(''); // For reCAPTCHA
    const navigate = useNavigate();

    const handleEmailChange = (e) => {
        setEmail(e.target.value);
    };

    const handlePasswordChange = (e) => {
        setPassword(e.target.value);
    };

    const handleRecaptchaChange = (token) => {
        setRecaptchaResponse(token); // Store the reCAPTCHA token
      }

    const handleLogin = async () => {
        let responseData = null;
        let response = null;
        
        try {
            response = await verifyCaptcha(recaptchaResponse); // reCAPTCHA verification
            responseData = await adminLogin(email, password); // Use the adminLogin function from loginService.js
                
            if (response && responseData.success && responseData.user_role === 'Admin') {
                setLoggedIn(true);
                setUserName(responseData.user_name);
                setUserRole(responseData.user_role);

                Cookies.set('user_name', responseData.user_name);

                navigate('/TwoFactorAuthentication');
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
            <>
            {errorMessage && <div className="error-message">{errorMessage}</div>}
                <LoginForm
                email={email}
                password={password}
                handleEmailChange={handleEmailChange}
                handlePasswordChange={handlePasswordChange}
                handleLogin={handleLogin}
                role={"admin"} // Specify the role as "admin"
                />
                <ReCAPTCHA
                sitekey="6Lf0zcsoAAAAAItrGtc2tjuTnu8rt3BBojtI9nr5"
                onChange={handleRecaptchaChange}
                />
            </>
            )}
        </div>
    );
}

export default AdminLogin;
