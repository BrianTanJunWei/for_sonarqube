import React, { useState } from 'react';
import '../css/createaccount.css';
import { useNavigate } from 'react-router-dom';
import { validateAge, validateEmail, validatePassword, validatePhoneNumber, validateConfirmPassword, validateCaptcha , validateName, validateImageFile} from '../Components/CreateAccountValidation';
import CreateAccountForm from '../Components/CreateAccountForm';
import { registerUser, verifyCaptcha } from '../services/Services';
import ReCAPTCHA from 'react-google-recaptcha';

const CreateAccount = () => {
  const [name, setName] = useState('');
  const [age, setAge] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [role, setRole] = useState('seller');
  const [profilePicture, setProfilePicture] = useState(null);
  const [passwordValidationMessage, setPasswordValidationMessage] = useState('');
  const [phoneNumber, setPhoneNumber] = useState('');
  const [phoneNumberError, setPhoneNumberError] = useState('');
  const [recaptchaResponse, setRecaptchaResponse] = useState(''); // For reCAPTCHA
  const navigate = useNavigate();

  const handleNameChange = (e) => {
    const newName = e.target.value;
    if (newName.length <= 25) {
      setName(newName);
    }
  };

  const handleProfilePictureChange = (e) => {
    const selectedFile = e.target.files[0];
    setProfilePicture(selectedFile);
  };

  const handlePhoneNumberChange = (e) => {
    const newPhoneNumber = e.target.value;
    setPhoneNumber(newPhoneNumber);
  };

  const handleEmailChange = (e) => {
    setEmail(e.target.value);
  };

  const handlePasswordChange = (e) => {
    const newPassword = e.target.value;
    setPassword(newPassword);
  };

  const handleConfirmPasswordChange = (e) => {
    setConfirmPassword(e.target.value);
  };

  const handleRoleChange = (e) => {
    setRole(e.target.value);
  };

  const handleRecaptchaChange = (token) => {
    setRecaptchaResponse(token); // Store the reCAPTCHA token
  }

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validate form fields using the validation functions
    const ageValidationMessage = validateAge(age);
    const emailValidationMessage = validateEmail(email);
    const passwordValidationMessage = validatePassword(password);
    const phoneNumberValidationMessage = validatePhoneNumber(phoneNumber);
    const confirmPasswordValidationMessage = validateConfirmPassword(password, confirmPassword);
    const captchaValidationMessage = validateCaptcha(recaptchaResponse);
    const nameValidationMessage = validateName(name);
    const ImageValidationMessage = validateImageFile(profilePicture)

    if (
      ageValidationMessage ||
      emailValidationMessage ||
      passwordValidationMessage ||
      phoneNumberValidationMessage ||
      confirmPasswordValidationMessage ||
      captchaValidationMessage ||
      nameValidationMessage ||
      ImageValidationMessage
    ) {
      alert(
        ageValidationMessage ||
          emailValidationMessage ||
          passwordValidationMessage ||
          phoneNumberValidationMessage ||
          confirmPasswordValidationMessage ||
          captchaValidationMessage || 
          nameValidationMessage ||
          ImageValidationMessage
      );
      return;
    }

    e.preventDefault();
    const registrationData = new FormData();
    registrationData.append('name', name);
    registrationData.append('age', age);
    // Append phone number to registrationData
    registrationData.append('phoneNumber', phoneNumber);
    registrationData.append('email', email);
    registrationData.append('password', password);
    registrationData.append('role', role);

    // Only append profilePicture if it's not null
    if (profilePicture !== null) {
      registrationData.append('profilePicture', profilePicture);
    }
   // const registrationSuccessful = await registerUser(registrationData);
    try {
      const responseData = await verifyCaptcha(recaptchaResponse); // reCAPTCHA verification
      const response = await fetch('/register', {
        method: 'POST',
        body: registrationData,
      });
      
      if (response.ok) {
        console.log('Registration successful');
        navigate('/QrCode');
      } else {
        // Check the response for specific error messages
        const responseData = await response.json();
        if (responseData.error === 'Email already exists') {
          // Display an error message for email existence
          alert('Email already exists');
        } else if (responseData.error === 'Phone number already exists') {
          // Display an error message for phone number existence
          alert('Phone number already exists');
        }else if (responseData.error === 'Name already exists') {
          // Display an error message for phone number existence
          alert('Name already exists');
        } else if (responseData.error === 'Invalid file format. Allowed formats: .jpg, .jpeg, .png') {
          // Display an error message for phone number existence
          alert('Invalid file format. Allowed formats: .jpg, .jpeg, .png');
        } else if (responseData.error === 'Username already exists') {
          // Display an error message for phone number existence
          alert('Phone number already exists');
        } else {
          console.error('Registration failed');
        }
      }
    } catch (error) {
      console.error('Error during registration:', error);
    }

  };

  return (
    <div className="create-account-container">
      <h2>Create Account</h2>
      <CreateAccountForm
        // Pass the state and event handlers as props to CreateAccountForm
        name={name}
        age={age}
        email={email}
        password={password}
        confirmPassword={confirmPassword}
        role={role}
        phoneNumber={phoneNumber}
        phoneNumberError={phoneNumberError}
        setName={setName}
        setAge={setAge}
        setEmail={setEmail}
        setPassword={setPassword}
        setConfirmPassword={setConfirmPassword}
        setRole={setRole}
        setPhoneNumber={setPhoneNumber}
        setPhoneNumberError={setPhoneNumberError}
        handleNameChange={handleNameChange}
        handleProfilePictureChange={handleProfilePictureChange}
        handlePhoneNumberChange={handlePhoneNumberChange}
        handleEmailChange={handleEmailChange}
        handlePasswordChange={handlePasswordChange}
        handleConfirmPasswordChange={handleConfirmPasswordChange}
        handleRoleChange={handleRoleChange}
        onSubmit={handleSubmit} // Pass the handleSubmit function as a prop
      />
      <ReCAPTCHA
        sitekey="6Lf0zcsoAAAAAItrGtc2tjuTnu8rt3BBojtI9nr5"
        onChange={handleRecaptchaChange}
      />
    </div>
  );
}

export default CreateAccount;
