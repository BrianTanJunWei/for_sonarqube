import Cookies from "js-cookie";
import { jwtDecode } from "jwt-decode";

// Sessionvalidation.js
export async function verifySession() {
  let userId = '';
  let userRole = '';
  let storedToken = '';
  // Setting Cookies up
  const cookieSession = Cookies.get('session');
  if (cookieSession){
    if (cookieSession.charAt(0) === 'e'){
      const sessionCookie = jwtDecode(cookieSession, { header: true });
      userId = sessionCookie.user_id;
      userRole = sessionCookie.user_role;
      storedToken = sessionCookie.session_token;
    }
  }
  
    if (storedToken && userId && userRole) {
      return fetch('/verify-session-token', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          session_token: storedToken,
          user_id: userId,
          user_role: userRole,
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (!data.valid) {
            // Session is not valid, clear Cookies and redirect to login
            Cookies.remove('session');
            window.location.href = '/Login';
          }
        })
        .catch((error) => {
          console.error('Error while verifying session token:', error);
        });
    } else {  
      // If any of the necessary items are missing in local storage, return a Promise that rejects
      console.error('Missing session token, user ID, or user role');
      // return Promise.reject('Missing session token, user ID, or user role');
    }
  }
  