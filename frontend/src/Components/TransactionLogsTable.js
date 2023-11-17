import React from "react";

function TransactionLogsTable({ transactionLogs }) {
  return (
    <div className="logs-table">
      <table>
        <thead>
          <tr>
            <th>Order ID</th>
            <th>Buyer ID</th>
            <th>Time</th>
            <th>Total Cost</th>
            <th>Products</th>
          </tr>
        </thead>
        <tbody>
          {transactionLogs.map((transaction) => (
            <tr key={transaction.OrderID}>
              <td>{transaction.OrderID}</td>
              <td>{transaction.BuyerID}</td>
              <td>{transaction.Time}</td>
              <td>${transaction.TotalCost}</td>
              <td>
                {Object.keys(transaction.Products).map((productID) => (
                  <div key={productID}>
                    {transaction.Products[productID].ProductName} ({transaction.Products[productID].QuantityOrdered})
                  </div>
                ))}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default TransactionLogsTable;
