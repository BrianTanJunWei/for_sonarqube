import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Link, useNavigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import App from './CartManagement';
import Cookies from "js-cookie";
import { jwtDecode } from "jwt-decode";
import { verifySession } from "./Sessionvalidation";

function Header() { 
  const [loggedIn, setLoggedIn] = useState(false);
  const navigate = useNavigate(); // Initialize navigate from React Router
  let userId = '';
  let userRole = '';
  
  // Setting Cookies up
  const cookieSession = Cookies.get('session');
  if(cookieSession) {
    if (cookieSession.charAt(0) === 'e'){
      const sessionCookie = jwtDecode(cookieSession, { header: true });
      userId = sessionCookie.user_id;
      userRole = sessionCookie.user_role;
    }
}
  
  const linkStyle = {
    textDecoration: 'none', // Remove underline
  };
  const handleLogout = async () => {
    try {
      // You can send a logout request to your Flask backend to invalidate the user's session or token.
      const response = await fetch('/logout', {
        method: 'POST', // You can use the appropriate HTTP method
        // Add any necessary headers, like authentication headers, if required
      });

      if (response.ok) {
        // Assuming your backend returns a success status on successful logout
        // Remove user_id and user_role from sessionStorage
        Cookies.remove('session');

        // Update the state to indicate that the user is logged out
        setLoggedIn(false);
        // Redirect the user to the login page or any other appropriate page
        navigate('/'); // Replace '/login' with your actual login page route
      } else {
        console.error('Logout failed');
      }
    } catch (error) {
      console.error('Error during logout:', error);
    }
  };

  const [openedDrawer, setOpenedDrawer] = useState(false);

  function toggleDrawer() {
    setOpenedDrawer(!openedDrawer);
  }

  function changeNav(event) {
    if (openedDrawer) {
      setOpenedDrawer(false);
    }
  }

  return (
    <header>
      <nav className="navbar fixed-top navbar-expand-lg navbar-light bg-white border-bottom">
        <div className="container-fluid">
          <Link className="navbar-brand" to="/" onClick={changeNav}>
            <span className="ms-2 h5">FerrisWheel</span>
          </Link>

          <button
            className="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarNav"
            aria-controls="navbarNav"
            aria-expanded={openedDrawer ? "true" : "false"} // Set aria-expanded based on state
            aria-label="Toggle navigation"
            onClick={toggleDrawer} // Add onClick to toggle the drawer
          >
            <span className="navbar-toggler-icon"></span>
          </button>

          <div className={"navbar-collapse offcanvas-collapse " + (openedDrawer ? "open" : "")}>
            <ul className="navbar-nav me-auto mb-lg-0">
              <li className="nav-item">
                {/* Insert some stuff */}
              </li>
            </ul>

            {userRole === "Buyer" && <App />}
            {/* Shopping Cart button */}

            {/* Only for seller view */}
            {userRole === "Seller" && (
              <ul className="navbar-nav mx-auto">
                <li className="nav-item">
                  <Link to="/SellerView" className="nav-link">
                    Home
                  </Link>
                </li>
                <li className="nav-item">
                  <Link to="/SellerProducts" className="nav-link">
                    My Products
                  </Link>
                </li>
                <li className="nav-item">
                  <Link to="/AddProducts" className="nav-link">
                    Add Products
                  </Link>
                </li>
                <li className="nav-item">
                  <Link to="/Notifications" className="nav-link">
                    Notifications
                  </Link>
                </li>
              </ul>
            )}

            <ul className="navbar-nav mb-2 mb-lg-0">
              <li className="nav-item dropdown">
                <a
                  href="!#"
                  className="nav-link dropdown-toggle"
                  data-toggle="dropdown"
                  id="userDropdown"
                  role="button"
                  data-bs-toggle="dropdown"
                  aria-expanded={openedDrawer ? "true" : "false"} // Set aria-expanded based on state
                >
                  <FontAwesomeIcon icon={["fas", "user-alt"]} />
                </a>
                <ul className="dropdown-menu dropdown-menu-end" aria-labelledby="userDropdown">
                  {userId ? (
                    <li>
                      <button onClick={handleLogout} className="dropdown-item">
                        Logout
                      </button>
                      <Link to="/Profile" style={linkStyle}>
                        <button className="dropdown-item">Profile</button>
                      </Link>
                    </li>
                  ) : (
                    <li>
                      <Link to="/Login" className="dropdown-item" onClick={changeNav}>
                        Login
                      </Link>
                      <Link to="/CreateAccount" className="dropdown-item" onClick={changeNav}>
                        Sign Up
                      </Link>
                    </li>
                  )}
                </ul>
              </li>
            </ul>
          </div>
        </div>
      </nav>
    </header>
  );
}
export default Header;
