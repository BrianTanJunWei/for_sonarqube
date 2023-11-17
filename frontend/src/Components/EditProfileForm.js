import React from 'react';
import { Link  } from 'react-router-dom';
const ProfileForm = ({
  name,
  email,
  age,
  phoneNumber,
  nameError,
  emailError,
  phoneNumberError,
  handleInputChange,
  setNewProfilePicture,
  handleSubmit,
}) => (
  <div className="container mt-5">
    <h2 className="text-center">Edit Profile</h2>
    <form className="col-md-6 mx-auto mt-4" onSubmit={handleSubmit}>
      <div className="mb-3">
        <label htmlFor="name" className="form-label">Name:</label>
        <input
          type="text"
          className={`form-control ${nameError ? 'is-invalid' : ''}`}
          name="name"
          value={name}
          required
          onChange={handleInputChange}
        />
        {nameError && (
          <div className="invalid-feedback">{nameError}</div>
        )}
      </div>
      <div className="mb-3">
        <label htmlFor="phonenumber" className="form-label">Phone Number:</label>
        <input
          type="text"
          className={`form-control ${phoneNumberError ? 'is-invalid' : ''}`}
          name="phonenumber"
          value={phoneNumber}
          pattern="[0-9]{8}"
          required
          placeholder="Enter your 8-digit phone number"
          title="Enter your 8-digit phone number"
          onChange={handleInputChange}
        />
        {phoneNumberError && (
          <div className="invalid-feedback">{phoneNumberError}</div>
        )}
      </div>
      <div className="mb-3">
        <label htmlFor="email" className="form-label">Email:</label>
       {email}
      </div>
      <div className="mb-3">
        <label htmlFor="age" className="form-label">Age:</label>
        {age}
      </div>
      <div className="mb-3">
        <label htmlFor="profilePicture" className="form-label">Profile Picture:</label>
        <input
          type="file"
          accept="image/*"
          className="form-control-file"
          onChange={(e) => setNewProfilePicture(e.target.files[0])}
        />
      </div>
      <button type="submit" className="btn btn-primary" >
        Save Changes
      </button>
      <Link to="/Profile">
        <button type="button" className="btn btn-primary" >
          Back
        </button>
      </Link>
    </form>
  </div>
);

export default ProfileForm;
