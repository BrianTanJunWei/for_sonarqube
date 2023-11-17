import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import ProfileForm from '../Components/EditProfileForm';
import Services from '../services/Services';
import Cookies from 'js-cookie';
import { jwtDecode } from 'jwt-decode';

const EditProfile = () => {
  const location = useLocation();
  const navigate = useNavigate();

  // Extract user data from the location state, or use default values
  const userData = location.state?.userData || { name: '', email: '', age: '', phonenumber: '' };

  const [newProfilePicture, setNewProfilePicture] = useState(null);

  // Maintain the input values in component state
  const [editedUserData, setEditedUserData] = useState(userData);
  const [emailError, setEmailError] = useState('');
  const [nameError, setNameError] = useState('');
  const [phoneNumberError, setPhoneNumberError] = useState('');

  let userId = '';
  // Setting Cookies up
  const cookieSession = Cookies.get('session');
  if (cookieSession){
    const sessionCookie = jwtDecode(cookieSession, { header: true });
    userId = sessionCookie.user_id;
  }

  // Function to handle form input changes
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setEditedUserData({
      ...editedUserData,
      [name]: value,
    });
  };

  const validateEmail = (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+/;
    if (!emailRegex.test(email)) {
      setEmailError('Invalid email format');
    } else {
      setEmailError('');
    }
  };

  const validateName = (name) => {
    if (name.length > 20) {
      setNameError('Name cannot be more than 20 characters');
    } else {
      setNameError('');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
  
    // Validate email and name
    validateEmail(editedUserData.email);
    validateName(editedUserData.name);
  
    // Validate phone number
    const phoneNumberPattern = /^[89]\d{7}$/;
    if (!phoneNumberPattern.test(editedUserData.phonenumber)) {
      setPhoneNumberError('Phone number must have 8 digits and start with 8 or 9');
      return; // Add this return statement to prevent further execution
    } else {
      // Check if the phone number already exists
      try {
        // IMPORTANT! REMEMBER TO CHANGE IF NOT USING USERID FROM COOKIES!!!
        const response = await Services.checkPhoneNumberExists(editedUserData.phonenumber, userId);
        if (response.exists) {
          setPhoneNumberError('Phone number is already in use.');
          return; // Add this return statement to prevent further execution
        } else {
          setPhoneNumberError('');
        }
      } catch (error) {
       
        console.error('Error checking phone number existence:', error);
      }
    }
  
    // Check if there are any validation errors
    if (emailError || nameError || phoneNumberError) {
      alert('Validation errors. Please correct them before saving.');
      return;
    }
    // Create a FormData object to send data including the profile picture
    const formData = new FormData();
    formData.append('name', editedUserData.name);
    formData.append('email', editedUserData.email);
    formData.append('phonenumber', editedUserData.phonenumber);
    if (newProfilePicture) {
      formData.append('profilePicture', newProfilePicture);
    } else {
      formData.append('profilePicture', userData.profilePicture);
    }
  
    try {
      const success = await Services.updateProfile(formData);
      if (success) {
        console.log('Update successful');
        navigate('/Profile');
        alert('Profile Updated');
      }
    } catch (error) {
      alert('Please Update valid credentials/picture format')
      console.error('Error during profile update:', error);
    }
  };

  return (
    <ProfileForm
      name={editedUserData.name}
      email={editedUserData.email}
      age={editedUserData.age}
      phoneNumber={editedUserData.phonenumber}
      nameError={nameError}
      emailError={emailError}
      phoneNumberError={phoneNumberError}
      handleInputChange={handleInputChange}
      setNewProfilePicture={setNewProfilePicture}
      handleSubmit={handleSubmit}
    />
  );
};

export default EditProfile;
