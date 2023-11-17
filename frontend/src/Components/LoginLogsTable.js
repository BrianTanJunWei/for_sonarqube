import React from "react";

function LoginLogsTable({ loginLogs }) {
  return (
    <div className="col-lg-9">
      <h1 className="main-title">Login Logs</h1>
      <div className="row">
        <div className="col-md-12">
          <div className="scrollable-container">
            <table className="logs-table">
              <tbody>
                {loginLogs.map((log) => (
                  <tr key={log.key}>
                    <td>{log.entry}</td>
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

export default LoginLogsTable;
