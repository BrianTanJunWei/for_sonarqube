import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link, useNavigate } from 'react-router-dom';
import '../css/profile.css';
import UserProfileForm from '../Components/UserProfileForm';
import { fetchUserProfile } from '../services/Services';
import { verifySession } from '../Components/Sessionvalidation';

function Profile() {
  const [userData, setUserData] = useState({
    name: '',
    email: '',
    age: '',
    phonenumber: '',
    profilePicture: '',
  });
  const navigate = useNavigate();

  useEffect(() => {
    verifySession();
    // Call the service function to fetch user profile data
    fetchUserProfile()
      .then((response) => {
        setUserData(response.data);
        console.log('Profile Picture URL:', response.data.profilePicture);
      })
      .catch((error) => {
        console.error('Error fetching user data:', error);
      });
  }, []);
  const handleEditProfile = () => {
    navigate('/EditProfile', { state: { userData } });
  };

  const handleChangePassword = () => {
    navigate('/ChangePassword');
  };

  return (
    <div className="container d-flex justify-content-center align-items-center mt-5">
      <UserProfileForm
        userData={userData}
        handleEditProfile={handleEditProfile}
        handleChangePassword={handleChangePassword}
      />
    </div>
  );
}

export default Profile;
