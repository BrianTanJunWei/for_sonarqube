// ChangePassword.js
import React, { useState } from 'react';
import { Container, Card, CardBody } from 'reactstrap';
import PasswordChangeForm from '../Components/PasswordChangeForm';
import { changePassword } from '../services/Services'; // Import the service function
import '../css/changepassword.css';
import { useNavigate } from 'react-router-dom';

function ChangePassword() {
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const navigate = useNavigate();

  const handleCurrentPasswordChange = (e) => {
    setCurrentPassword(e.target.value);
  };

  const handleNewPasswordChange = (e) => {
    setNewPassword(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      await changePassword(currentPassword, newPassword); // Call the API service function
      console.log('Password changed successfully');
    } catch (error) {
      console.error('Error:', error.message);
    }

    setCurrentPassword('');
    setNewPassword('');
    navigate('/Profile');
  };

  return (
    <Container style={{ maxWidth: '1000px', maxHeight: '700px' }}>
      <Card className="password-container">
        <CardBody style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginTop: '100px' }}>
          <h2>Change Password</h2>
          <PasswordChangeForm
            currentPassword={currentPassword}
            newPassword={newPassword}
            onCurrentPasswordChange={handleCurrentPasswordChange}
            onNewPasswordChange={handleNewPasswordChange}
            onSubmit={handleSubmit}
          />
        </CardBody>
      </Card>
    </Container>
  );
}

export default ChangePassword;
