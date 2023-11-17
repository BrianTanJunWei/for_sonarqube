import React ,{ useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { QRCodeSVG } from 'qrcode.react';
import { getURI } from '../services/Services';

function QrCode() {
    const [uri, setURI] = useState(null);

    useEffect(() => {
        async function fetchURI() {
            try {
                const response = await getURI();
                setURI(response);
            } catch (error) {
                console.error('Error fetching URI: ', error);
            }
        }
        fetchURI();
    }, []);

  return (
    <div className="container"  style={{ marginTop: "120px" }}>
      <h1>2FA</h1>
      <h2>Google Authentication</h2>
      <div className="form-group d-inline">
        <label>Scan QRCODE with Google Authenticator and verify your account in email</label>
        <div>
        <QRCodeSVG
          value={uri}
        />
        </div>
      </div>
      <Link to ="/Login">
        <button className="btn btn-primary">Login</button>
      </Link>
    </div>
  );
}

export default QrCode;
