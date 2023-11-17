// RoutewithSessionVerifier.js
import React, { useEffect } from 'react';
import { verifySession } from './Sessionvalidation';

function RoutewithSessionVerifier({ children }) {
  useEffect(() => {
    verifySession()
      .then(() => {
        console.log('Session verified successfully.');
      })
      .catch((error) => {
        console.error('Session verification failed:', error);
      });
  }, []);

  return children;
}

export default RoutewithSessionVerifier;
