import { BrowserRouter as Router, Route, Routes, useNavigate } from "react-router-dom"; // Import useNavigate
import Login from "./pages/Login";
import Other from "./pages/AdminLogin";
import AdminView from "./pages/AdminView";
import TransactionLogs from "./pages/TransactionLogs";
import AccountStatus from "./pages/AccountStatus";
import LoginLogs from "./pages/LoginLogs";
import React, { useState, useEffect } from 'react'; // Remove useNavigate
import CreateAccount from "./pages/CreateAccount";
import "./App.css"
import BuyerView from "./pages/BuyerView";
import Checkout from "./pages/Checkout";
import SellerView from "./pages/SellerView";
import SellerProducts from "./pages/SellerProducts";
import EditProducts from "./pages/EditProducts";
import AddProducts from "./pages/AddProducts";
import Notifications from "./pages/Notifications";
import Template from "./pages/Template";
import "./css/login.css"
import TwoFactorAuthentication from "./pages/TwoFactorAuthentication";
import ForgetPassword from "./pages/ForgetPassword";
import Profile from "./pages/Profile";
import EditProfile from "./pages/EditProfile";
import ChangePassword from "./pages/ChangePassword";
import RouteGuard from "./Components/RouteGuard";
import RoutewithSessionVerifier from "./Components/RoutewithSessionVerifier";
import QrCode from "./pages/QrCode";
import Cookies from "js-cookie";

function App() {

  const [loggedIn, setLoggedIn] = useState(false);
  const [validSession, setValidSession] = useState(false);
  const [checkDone, setCheckDone] = useState(false); // Track if the check has been done

  useEffect(() => {
   
     const handleBeforeUnload = async (event) => {
    // Check if the event is a page refresh or an actual window close
      if (event.clientY < 0) {
        // This means the user is closing the window/tab
        try {
          await fetch('/logout', {
            method: 'POST',
            // Add any necessary headers, like authentication headers, if required
          });
        } catch (error) {
          console.error('Error during logout:', error);
        }
      }
	 };

    window.addEventListener('beforeunload', handleBeforeUnload);

    // Clean up the event listener when the component unmounts
    return () => {
      window.removeEventListener('beforeunload', handleBeforeUnload);
    };
  }, [checkDone]);

  return (
    
    <Template>
    
      <Routes>
        <Route path="/" element={<BuyerView />} />
        <Route path="/CreateAccount" element={<CreateAccount />} />
        <Route path="/QrCode" element={<QrCode />} />
        <Route path="/Login" element={<Login />} />
        <Route path="/TwoFactorAuthentication" element={<TwoFactorAuthentication />} />
        <Route path="/ForgetPassword" element={<ForgetPassword />} />
        <Route path="/66554" element={<Other />} />
        {/* Protected routes */}
        
        <Route
          path="/EditProfile"
          element={
            <RoutewithSessionVerifier>
            <RouteGuard roles={['Buyer', 'Seller', 'Admin']}>
              
              <EditProfile />
          
            </RouteGuard>
            </RoutewithSessionVerifier>
          }
        />
         
        <Route
          path="/ChangePassword"
          element={
            <RoutewithSessionVerifier>
            <RouteGuard roles={['Buyer', 'Seller', 'Admin']}>
              <ChangePassword />
            </RouteGuard>
            </RoutewithSessionVerifier>
          }
        />

        <Route
          path="/BuyerView"
          element={
            <RoutewithSessionVerifier>
            <RouteGuard roles={['Buyer']}>
              <BuyerView />
            </RouteGuard>
            </RoutewithSessionVerifier>
          }
        />
        <Route
          path="/Checkout"
          element={
            <RoutewithSessionVerifier>
            <RouteGuard roles={['Buyer']}>
              <Checkout />
            </RouteGuard>
            </RoutewithSessionVerifier>
          }
        />
        {/* <Route
          path="/QrCode"
          element={
            <RoutewithSessionVerifier>
            <RouteGuard roles={['Buyer', 'Seller', 'Admin']}>
              <QrCode />
            </RouteGuard>
            </RoutewithSessionVerifier>
          }
        /> */}
         {/* <Route
          path="/TwoFactorAuthentication"
          element={
            <RoutewithSessionVerifier>
            <RouteGuard roles={['Buyer', 'Seller', 'Admin']}>
              <TwoFactorAuthentication />
            </RouteGuard>
            </RoutewithSessionVerifier>
          }
        /> */}
        <Route
          path="/EditProducts"
          element={
            <RoutewithSessionVerifier>
            <RouteGuard roles={['Seller']}>
              <EditProducts />
            </RouteGuard>
            </RoutewithSessionVerifier>
          }
        />
        <Route
          path="/SellerProducts"
          element={
            <RoutewithSessionVerifier>
            <RouteGuard roles={['Seller']}>
              <SellerProducts />
            </RouteGuard>
            </RoutewithSessionVerifier>
          }
        />
        <Route
          path="/AddProducts"
          element={
            <RoutewithSessionVerifier>
            <RouteGuard roles={['Seller']}>
              <AddProducts />
            </RouteGuard>
            </RoutewithSessionVerifier>
          }
        />
        <Route
          path="/SellerView"
          element={
            <RoutewithSessionVerifier>
            <RouteGuard roles={['Seller']}>
              <SellerView />
            </RouteGuard>
            </RoutewithSessionVerifier>
          }
        />
        <Route
          path="/Notifications"
          element={
            <RoutewithSessionVerifier>
            <RouteGuard roles={['Seller']}>
              <Notifications />
            </RouteGuard>
            </RoutewithSessionVerifier>
          }
        />
        <Route
          path="/Profile"
          element={
            <RoutewithSessionVerifier>
            <RouteGuard roles={['Buyer', 'Seller', 'Admin']}>
              <Profile />
            </RouteGuard>
            </RoutewithSessionVerifier>
          }
        />
        <Route
          path="/AdminView"
          element={
            <RoutewithSessionVerifier>
            <RouteGuard roles={['Admin']}>
              <AdminView />
            </RouteGuard>
            </RoutewithSessionVerifier>
          }
        />
        <Route
          path="/AccountStatus"
          element={
            <RoutewithSessionVerifier>
            <RouteGuard roles={['Admin']}>
              <AccountStatus />
            </RouteGuard>
            </RoutewithSessionVerifier>
          }
        />
        <Route
          path="/LoginLogs"
          element={
            <RoutewithSessionVerifier>
            <RouteGuard roles={['Admin']}>
              <LoginLogs />
            </RouteGuard>
            </RoutewithSessionVerifier>
          }
        />
        <Route
          path="/TransactionLogs"
          element={
            <RoutewithSessionVerifier>
            <RouteGuard roles={['Admin']}>
              <TransactionLogs />
            </RouteGuard>
            </RoutewithSessionVerifier>
          }
        />
      </Routes>
     
    </Template>
   
  );
}

export default App;