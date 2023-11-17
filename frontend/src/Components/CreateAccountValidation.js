
export function validateAge(age) {
   // Parse the input as an integer
   const parsedAge = parseInt(age, 10);

   // Convert the parsed integer back to a string and compare with the original input
   if (parsedAge.toString() !== age) {
       return 'Invalid input: age should not contain leading zeros or non-numeric characters';
   }

   // Perform the range check
   if (parsedAge < 18 || parsedAge > 80) {
       return 'Age must be between 18 and 80';
   }

   // If all checks pass, return an empty string
   return '';
  }
  
  export function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      return 'Invalid email format';
    }
    return '';
  }
  export function validateConfirmPassword(password, confirmPassword) {
    if (password !== confirmPassword) {
      return 'Password and Confirm Password do not match.';
    }
    return '';
  }
  export function validatePassword(password) {
    const minLength = 12;
    const hasSpecialChar = /[!@#$%^&*()_+{}\[\]:;<>,.?~\\-]/.test(password);
    const hasNumber = /\d/.test(password);
    const hasUpperCase = /[A-Z]/.test(password);
  
    if (
      password.length < minLength ||
      !hasSpecialChar ||
      !hasNumber ||
      !hasUpperCase
    ) {
      return 'Password must have 12 characters minimum, 1 special character, 1 number, and 1 capital letter.';
    }
    return '';
  }
  
  export function validatePhoneNumber(phoneNumber) {
    const phoneNumberPattern = /^[89]\d{7}$/;
    if (!phoneNumberPattern.test(phoneNumber)) {
      return 'Phone number must be 8 digits and start with 8 or 9';
    }
    return '';
  }

  export function validateCaptcha(recaptchaResponse) {
    if (recaptchaResponse === '') {
      return 'reCAPTCHA is not entered';
    }
    return '';
  }

  export function validateName(name) {
    // Type check
    if (typeof name !== 'string') {
        return 'Name must be a text string';
    }

    // Length check
    const minLength = 2;
    const maxLength = 15;
    if (name.length < minLength || name.length > maxLength) {
        return `Name must be between ${minLength} and ${maxLength} characters long`;
    }

    // Character whitelisting with a regular expression
    if (!/^[A-Za-z0-9' -]+$/.test(name)) {
      return 'Name contains invalid characters';
    }

    // If all checks pass, return an empty string indicating no error
    return '';
}

export function validateImageFile(file) {
  // Check if the file is provided
  if (!file) {
      return 'No file provided';
  }

  // Escape special characters in filename
  const escapedFileName = file.name.replace(/[<>:"/\\|?*\x00-\x1F]/g, '_');

  // Check file size (e.g., limit to 5MB)
  if (file.size > 5 * 1024 * 1024) {
      return 'File size exceeds 5MB';
  }

  // Check file type (MIME type)
  const validTypes = ['image/jpeg', 'image/png'];
  if (!validTypes.includes(file.type)) {
      return 'Invalid file type';
  }

  // Client-side file extension check
  const validExtensions = ['.jpeg', '.jpg', '.png'];
  const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
  if (!validExtensions.includes(fileExtension)) {
      return 'Invalid file extension';
  }
  // If all checks pass, return an empty string indicating no error
  return '';
}



  
  
  