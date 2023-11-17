import React from 'react';

function UserProfileForm({ userData, handleEditProfile, handleChangePassword }) {
  return (
    <div className="text-center">
      <img
        src={userData.profilePicture}
        style={{ height: '180px', marginTop: '20px' }}
        alt="Profile"
        className="img-fluid rounded-circle"
      />
      <h1 className="display-4">{userData.name}</h1>
      <ul className="list-group text-left">
        <li className="list-group-item">
          <strong>Email:</strong> {userData.email}
        </li>
        <li className="list-group-item">
          <strong>Phone Number:</strong> {userData.phonenumber}
        </li>
        <li className="list-group-item">
          <strong>Age:</strong> {userData.age}
        </li>
      </ul>
      <button onClick={handleEditProfile} className="btn btn-primary mt-3">
        Edit Profile
      </button>
      <button onClick={handleChangePassword} className="btn btn-primary mt-3">
        Change Password
      </button>
    </div>
  );
}

export default UserProfileForm;
