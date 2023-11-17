import React from 'react';

function CreateAccountForm({
  name,
  age,
  email,
  password,
  confirmPassword,
  role,
  profilePicture,
  phoneNumber,
  phoneNumberError,
  setName,
  setAge,
  setEmail,
  setPassword,
  setConfirmPassword,
  setRole,
  setPhoneNumber,
  handleNameChange,
  handleProfilePictureChange,
  handlePhoneNumberChange,
  handleEmailChange,
  handlePasswordChange,
  handleConfirmPasswordChange,
  handleRoleChange,
  onSubmit,
}) {
  return (
    <form className="create-account-form" onSubmit={onSubmit}>
      <div className="form-group">
        <label htmlFor="name">Name:</label>
        <input
          type="text"
          id="name"
          value={name}
          onChange={handleNameChange}
          required
          className="form-control"
        />
      </div>
      <div className="form-group">
        <label htmlFor="age">Age:</label>
        <input
          type="number"
          id="age"
          value={age}
          onChange={(e) => setAge(e.target.value)}
          required
          className="form-control"
        />
      </div>
      <div className="form-group">
        <label htmlFor="email">Email:</label>
        <input
          type="email"
          id="email"
          value={email}
          onChange={handleEmailChange}
          required
          className="form-control"
        />
      </div>
      <div className="form-group">
        <label htmlFor="phoneNumber">Phone Number:</label>
        <input
          type="number"
          id="phoneNumber"
          value={phoneNumber}
          onChange={handlePhoneNumberChange}
          required
          className="form-control"
        />
        {phoneNumberError && (
          <p className="error-message">{phoneNumberError}</p>
        )}
      </div>
      <div className="form-group">
        <label htmlFor="password">Password:</label>
        <input
          type="password"
          id="password"
          value={password}
          onChange={handlePasswordChange}
          required
          className="form-control"
        />
      </div>
      <div className="form-group">
        <label htmlFor="confirmPassword">Confirm Password:</label>
        <input
          type="password"
          id="confirmPassword"
          value={confirmPassword}
          onChange={handleConfirmPasswordChange}
          required
          className="form-control"
        />
      </div>
      <div className="form-group">
        <label>Choose your role:</label>
        <div>
          <label>
            <input
              type="radio"
              name="role"
              value="Seller"
              checked={role === 'Seller'}
              onChange={handleRoleChange}
            />{' '}
            Seller
          </label>
        </div>
        <div>
          <label>
            <input
              type="radio"
              name="role"
              value="Buyer"
              checked={role === 'Buyer'}
              onChange={handleRoleChange}
            />{' '}
            Buyer
          </label>
        </div>
      </div>
      <div className="form-group">
        <label htmlFor="profilePicture">Upload Profile Picture:</label>
        <input
          type="file"
          id="profilePicture"
          accept="image/*"
          onChange={handleProfilePictureChange}
          className="form-control"
        />
      </div>
      <button type="submit" className="submit-button">
        Create Account
      </button>
    </form>
  );
}

export default CreateAccountForm;
