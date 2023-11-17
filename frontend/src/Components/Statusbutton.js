import React from "react";

function StatusButton({ account, onClick }) {
  return (
    <div className="col-md-2">
      <table className="account-table">
        <thead>
          <tr>
          </tr>
        </thead>
        <tbody>
          <tr key={account.identifier}>
            <td>
              <button
                className={`status-button ${account.status ? "enabled" : "disabled"}`}
                onClick={onClick}
              >
                {account.status ? "Disable" : "Enable"}
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  );
}

export default StatusButton;
