import React from "react";
import "../css/AdminSidePanel.css"; // Import the CSS file

function AdminSidePanel() {
  // Define the links and content for the admin panel
  const adminLinks = [
    { text: "Home", link: "/AdminView" },
    { text: "Transaction Logs", link: "/TransactionLogs" },
    { text: "Login Logs", link: "/LoginLogs" },
    { text: "profile", link: "/Profile" },
    { text: "Account status", link: "/AccountStatus" },
  ];

  return (
    <div className="admin-side-panel">
      <ul>
        {adminLinks.map((link, index) => (
          <li key={index}>
            <a href={link.link}>{link.text}</a>
          </li>
        ))}
      </ul>
    </div>
  );

}

export default AdminSidePanel;
