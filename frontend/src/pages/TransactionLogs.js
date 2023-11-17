import React, { useEffect, useState } from "react";
import AdminSidePanel from "../Components/AdminSidePanel";
import TransactionLogsTable from "../Components/TransactionLogsTable";
import { fetchTransactionLogs } from "../services/Services";
import "../css/TransactionLogs.css";

function TransactionLogs() {
  const [transactionLogs, setTransactionLogs] = useState([]);

  useEffect(() => {
    // Fetch transaction logs data from the API module
    fetchTransactionLogs()
      .then((response) => {
        setTransactionLogs(response.data);
      })
      .catch((error) => {
        console.error("Error fetching transaction logs:", error);
      });
  }, []);

  return (
    <div className="container-fluid">
      <div className="row">
        <div className="col-lg-3">
          <AdminSidePanel />
        </div>
        <div className="col-lg-9">
          <h1 className="main-title">Transaction Logs</h1>
          <div className="logs-table-container">
            <TransactionLogsTable transactionLogs={transactionLogs} />
          </div>
        </div>
      </div>
    </div>
  );
}

export default TransactionLogs;
