import Cookies from 'js-cookie';
import React from 'react';
import { Navigate } from 'react-router-dom';
import { jwtDecode } from 'jwt-decode';

const RouteGuard = ({ roles, children }) => {
  let userRole = '';
  // Setting Cookies up
  const cookieSession = Cookies.get('session');
  if (cookieSession) {
    if (cookieSession.charAt(0) === 'e'){
      const sessionCookie = jwtDecode(cookieSession, { header: true });
      userRole = sessionCookie.user_role;
    }
  }
  const isLoggedIn = userRole !== '';


  if (!isLoggedIn) {
    // If the user is not logged in, redirect to the Login page
    return <Navigate to="/Login" replace />;
  }

  if (roles && roles.includes(userRole)) {
    // If the user has the required role, allow access to the route
    return children;
  } else if (userRole === 'Buyer') {
    // If the user is a Buyer but not allowed to access the route, redirect to BuyerView
    return <Navigate to="/BuyerView" replace />;
  } else if (userRole === 'Seller') {
    // If the user is a Seller but not allowed to access the route, redirect to SellerView
    return <Navigate to="/SellerView" replace />;
  }else if(userRole === 'Admin'){
    return <Navigate to="/AdminView" replace />;
  } else {
    // Handle other cases, e.g., unknown roles
    return <Navigate to="/Login" replace />;
  }
};

export default RouteGuard;
