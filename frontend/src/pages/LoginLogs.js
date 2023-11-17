import React, { useEffect, useState } from "react";
import AdminSidePanel from "../Components/AdminSidePanel";
import axios from "axios";
import "../css/LoginLogs.css";
import LoginLogsTable from "../Components/LoginLogsTable";
import { fetchLoginLogs } from "../services/Services";

function LoginLogs() {
    const [loginLogs, setLoginLogs] = useState([]);
    useEffect(() => {
        // Fetch login logs data from the API module
        fetchLoginLogs()
          .then((response) => {
            setLoginLogs(response.data);
          })
          .catch((error) => {
            console.error("Error fetching login logs:", error);
          });
      }, []);

    return (
        <div className="container-fluid">
          <div className="row">
            <div className="col-lg-3">
              <AdminSidePanel />
            </div>
            <LoginLogsTable loginLogs={loginLogs} /> {/* Use the new component here */}
          </div>
          </div>
      );
    }
  export default LoginLogs;