import React from "react";

function AccountTable({ accounts, header, field }) {
  return (
    <div className="col-md-2">
      <table className="account-table">
        <thead>
          <tr>
            <th>{header}</th>
          </tr>
        </thead>
        <tbody>
          {accounts.map((account) => (
            <tr key={account.identifier}>
              <td>{field(account)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default AccountTable;
