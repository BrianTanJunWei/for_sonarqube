import React, { useState } from 'react';
import ForgetPasswordForm from '../Components/ForgetPasswordForm';
import { resetPassword } from '../services/Services';

function ForgetPassword() {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');

  const handleResetPassword = async () => {
    try {
      const response = await resetPassword(email); // Call the resetPassword function

      setMessage(response);
    } catch (error) {
      setMessage(error.message);
    }
  };

  return (
    <div className="container mt-5">
      <div className="row justify-content-center">
        <div className="col-md-6">
          <ForgetPasswordForm
            email={email}
            setEmail={setEmail}
            handleResetPassword={handleResetPassword}
            message={message}
          />
        </div>
      </div>
    </div>
  );
}

export default ForgetPassword;
