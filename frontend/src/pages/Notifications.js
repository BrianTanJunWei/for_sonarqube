import React, { useState, useEffect } from 'react';
import { fetchSellerNotifications, deleteNotification } from "../services/Services";
import "../css/Notifications.css";
import Cookies from 'js-cookie';
import { jwtDecode } from 'jwt-decode';
import { verifySession } from '../Components/Sessionvalidation';

function Notifications() {
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(false);
  const [refresh, setRefresh] = useState(false);
  
  let userID = '';
  // Setting Cookies up
  const cookieSession = Cookies.get('session');
  if (cookieSession){
    const sessionCookie = jwtDecode(cookieSession, { header: true });
    userID = sessionCookie.user_id;
  }

  const fetchNotifications = async () => {
    try {
      setLoading(true);
      setNotifications([]);
      const response = await fetchSellerNotifications(userID);
      setNotifications(response);
    } catch (error) {
      console.error('Error fetching notifications:', error);
    } finally {
      setLoading(false);
    }
  }

  const handleDeleteNotification = async (notificationId) => {
    try {
      const isDeleted = await deleteNotification(userID, notificationId);
  
      if (isDeleted) {
        // Notification deleted successfully, update the notifications state
        const updatedNotifications = notifications.filter(
          (notification) => notification.NotifID !== notificationId
        );
        setNotifications(updatedNotifications);
        window.alert("Notification Successfully deleted");
      } else {
        window.alert("Failed to delete notification");
      }
    } catch (error) {
      console.error('Error deleting notification:', error);
    }
  }
  
  useEffect(() => {
    fetchNotifications();
    verifySession();
  }, [refresh]);

  return (
    <div className="container-fluid">
      <div className="row mb-4 mt-lg-3">
        <div className="col-lg-3"></div>
        <div className="col-lg-9">
          <h1 className="main-title">Notifications</h1>
          {loading ? (
            <p>Loading notifications...</p>
          ) : (
            <table>
              <tbody>
                {notifications.length > 0 ? (
                  notifications.map((notification) => (
                    <tr key={notification.NotifID}>
                      <td>
                        {`${notification.BuyerEmail} has purchased ${notification.Quantity} item(s) of ${notification.Product} at ${notification.Time}`}
                      </td>
                      <td>
                        <button className="delete-button" onClick={() => handleDeleteNotification(notification.NotifID)}>
                          Delete
                        </button>
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="2">You have no notifications</td>
                  </tr>
                )}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  );
}

export default Notifications;
