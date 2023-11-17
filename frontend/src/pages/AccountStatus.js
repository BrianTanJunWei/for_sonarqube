import React, { useEffect, useState } from "react";
import axios from "axios";
import AdminSidePanel from "../Components/AdminSidePanel";
import "../css/AccountStatus.css"; // Import your CSS file
import AccountTable from "../Components/AccountTable";
import StatusButton from "../Components/Statusbutton";

function formatDatetime(timestamp) {
  if (timestamp) {
    const options = {
      year: "2-digit",
      month: "2-digit",
      day: "2-digit",
      hour: "numeric",
      minute: "numeric",
      second: "numeric",
    };
    return new Date(timestamp).toLocaleDateString("en-GB", options);
  }
  return "None";
}

function AccountStatus() {
  const [accounts, setAccounts] = useState([]);

  useEffect(() => {
    // Fetch account data from the Flask backend
    axios
      .get("/get_accounts")
      .then((response) => {
        setAccounts(response.data);
      })
      .catch((error) => {
        console.error("Error fetching account data:", error);
      });
  }, []);

  const toggleAccountStatus = (accountId, accountRole) => {
    // Toggle the account status locally in the frontend
    const updatedAccounts = accounts.map((account) => {
      if (account.identifier === accountId) {
        return {
          ...account,
          status: !account.status, // Toggle the status
        };
      }
      return account;
    });
    setAccounts(updatedAccounts);

    // Send a POST request to the backend to update the status
    axios
      .post("/update_user_status", {
        userId: accountId,
        disabled: !accounts.find((account) => account.identifier === accountId)
          .status,
        role: accountRole, // Include the role
      })
      .then((response) => {
        console.log(response.data);
      })
      .catch((error) => {
        console.error("Error toggling account status:", error);
      });
  };

  return (
    <div className="container-fluid">
      <div className="row mb-4 mt-lg-3">
        <div className="col-lg-3">
          <AdminSidePanel />
        </div>
        <div className="col-lg-9">
          <h1 className="main-title">Account Status</h1>
          <div className="table-container">
            <table className="account-table">
              <thead>
                <tr>
                  <th>Identifier</th>
                  <th>User Role</th>
                  <th>Last Signed-In Date</th>
                  <th>Last Signed-Out Date</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {accounts.map((account) => (
                  <tr key={account.identifier}>
                    <td>{account.identifier}</td>
                    <td>{account.role}</td>
                    <td>{formatDatetime(account.last_signed_in)}</td>
                    <td>{formatDatetime(account.last_signed_out)}</td>
                    <td>
                      <StatusButton
                        account={account}
                        onClick={() => toggleAccountStatus(account.identifier, account.role)}
                      />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
  

}

export default AccountStatus;