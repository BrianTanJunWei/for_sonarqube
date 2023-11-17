// loginService.js
import axios from 'axios';

export async function login(email, password) {
    const loginData = {
      email: email,
      password: password,
    };
  
    try {
      const response = await fetch('/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(loginData),
      });
      if (response) {
        const responseData = await response.json();
        return responseData;
      } else {
        throw new Error('Network error or server issue');
      }
    } catch (error) {
      throw error;
    }
  }
  
  export async function generateSessionToken(user_id, user_role) {
    const generateTokenResponse = await fetch('/generate-session-token', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user_id: user_id,
        user_role: user_role,
      })
    });
  
    if (generateTokenResponse.ok) {
      const tokenData = await generateTokenResponse.json();
      return tokenData;
    } else {
      throw new Error('Failed to generate session token');
    }
  }
  
  export async function adminLogin(email, password) {
    const loginData = {
      email: email,
      password: password,
    };
  
    try {
      const response = await fetch('/AdminLogin', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(loginData),
      });
  
      if (response.ok) {
        const responseData = await response.json();
        return responseData;
      } else {
        throw new Error('Network error or server issue');
      }
    } catch (error) {
      throw error;
    }
  }
  
// Function to get account data
export function getAccounts() {
    const endpoint = "/get_accounts";
    return axios.get(endpoint);
  }
  
  // Function to update account status
  export function updateAccountStatus(userId, role, disabled) {
    const endpoint = "/update_user_status";
    return axios.post(endpoint, { userId, role, disabled });
  }
  
  export async function fetchAllProducts() {
    const response = await fetch("/FetchAllProducts");
    if (!response.ok) {
      throw new Error("Failed to fetch products");
    }
    return response.json();
  }
  

// src/services/productService.js
export async function addProduct(productData) {
  try {
    const response = await fetch("/add-product", {
      method: "POST",
      body: productData,
    });

    if (response.ok) {
      return response.json(); // Assuming the server returns JSON data upon success
    } else {
      throw new Error("Product failed to add");
    }
  } catch (error) {
    throw error;
  }
}


export async function fetchFilteredProducts(checkedBoxes) {
  // Create an array to store the updated product list
  const updatedProductList = [];

  for (const key in checkedBoxes) {
    if (checkedBoxes[key]) {
      try {
        // Perform an API request to get filtered products
        const response = await fetch("/FetchFilteredProducts/" + key);
        if (response.ok) {
          const data = await response.json();

          for (let k = 0; k < data.length; k++) {
            if (!updatedProductList.some((product) => product.ProductID === data[k].ProductID)) {
              updatedProductList.push(data[k]);
            }
          }
        } else {
          console.error("Error fetching products:", response.status);
        }
      } catch (error) {
        console.error("Error fetching products:", error);
      }
    }
  }

  return updatedProductList;
}
const updateProfile = async (formData) => {
  try {
    const response = await fetch('/updateProfile', {
      method: 'POST',
      body: formData,
    });

    if (response.ok) {
      return true;
    } else {
      const errorMessage = 'Update failed';
      throw new Error(errorMessage);
    }
  } catch (error) {
    throw error;
  }
};

export async function checkPhoneNumberExists(phoneNumber,user_id) {
  const requestData = {
    phoneNumber: phoneNumber,
    user_id:user_id
  };
  try {
    const response = await fetch('/checkPhoneNumberExists', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestData),
    });

    if (response.ok) {
      const responseData = await response.json();
      return responseData;
    } else {
      throw new Error('Network error or server issue');
    }
  } catch (error) {
    throw error;
  }
}

const exportObject = {
  updateProfile,
  checkPhoneNumberExists
};

export default exportObject;
// Function to fetch a single product by its ID
export async function fetchProductById(productId) {
  try {
    const response = await axios.get('/get-product/${productId}');
    return response.data;
  } catch (error) {
    console.error('Error fetching product:', error);
    throw error;
  }
}




export async function updateProduct(productId, productData) {
  try {
    const response = await axios.post(`/edit-product/${productId}`, productData);
    return response.data; // Assuming the response contains the updated product data
  } catch (error) {
    console.error('Error updating products:', error);
    throw error;
  }
}


export const changePassword = async (currentPassword, newPassword) => {
  try {
    const data = {
      currentPassword,
      newPassword,
    };

    const response = await fetch('/change_password', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (response.ok) {
      return 'Password changed successfully';
    } else {
      throw new Error('Password change failed');
    }
  } catch (error) {
    throw error;
  }
};


export const resetPassword = async (email) => {
  try {
    const response = await fetch('/forgot-password', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email }),
    });

    const data = await response.json();

    if (data.success) {
      return data.message;
    } else {
      throw new Error(`Error: ${data.error}`);
    }
  } catch (error) {
    throw new Error(`Error: ${error.message}`);
  }
};

// Define a function to fetch user profile data
export const fetchUserProfile = () => {
  return axios.get('/profile');
};

const fetchLoginLogs = () => {
  return axios.get("/login_logs");
};

const fetchTransactionLogs = () => {
  return axios.get("/transaction_logs");
};

export { fetchLoginLogs,fetchTransactionLogs };
// api.js

export async function fetchSellerProducts(sellerUid) {
  try {
    const response = await fetch(`/Sellerproducts?seller_uid=${sellerUid}`);
    if (response.ok) {
      const data = await response.json();
      return data;
    } else {
      throw new Error("Failed to fetch products.");
    }
  } catch (error) {
    console.error("Error fetching products:", error);
    throw error;
  }
}

export async function fetchSellerNotifications(sellerId) {
  try {
    const response = await fetch(`/get_notifications?seller_uid=${sellerId}`);
    if (response.ok) {
      const data = await response.json();
      return data;
    } else {
      throw new Error("Failed to fetch notifications.");
    }
  } catch (error) {
    console.error("Error fetching notifications:", error);
    throw error;
  }
}

// Function to delete a notification by its ID for a specific user
export const deleteNotification = async (userId, notificationId) => {
  try {
    const response = await fetch(`/delete-notification/${userId}/${notificationId}`, {
      method: "DELETE",
    });

    if (response.ok) {
      console.log("Notification deleted successfully!");
      return true;
    } else {
      console.error("Failed to delete notification.");
      return false;
    }
  } catch (error) {
    console.error("Error deleting notification:", error);
    return false;
  }
};


export async function fetchProductData(productId, userId) {
  try {
    const response = await fetch(`/get-product/${productId}`);
    if (response.ok) {
      const data = await response.json();
      return data;
    } else {
      console.error("Failed to fetch product.");
      return null;
    }
  } catch (error) {
    console.error("Error fetching product:", error);
    return null;
  }
}

export async function deleteProduct(productId) {
  try {
    const response = await fetch(`/delete-product/${productId}`, {
      method: "DELETE",
    });

    if (response.ok) {
      console.log("Product deleted successfully!");
      return true;
    } else {
      console.error("Failed to delete product.");
      return false;
    }
  } catch (error) {
    console.error("Error deleting product:", error);
    return false;
  }
}

export async function verifyCaptcha(recaptchaResponse) {
  try {
    const response = await axios.post('/verify-recaptcha', {
      recaptchaResponse: recaptchaResponse
    });
    const responseData = await response.data;
    return responseData.success;

  } catch (error) {
    console.error("reCAPTCHA verification failed", error);
    throw error;
  }
}

export async function getURI() {
  try{
    const uri = await axios.get('/getURI');
    const data = await uri.data;
    return data.uri;
    
  } catch (error) {
    console.error("Unable to get URI", error);
    throw error;
  }
}

export async function verify2FA(twoFA) {
  const twoFAData = {
    twoFA: twoFA,
  };

  try{
    const response = await fetch('/verify2FA', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(twoFAData),
    });
    if (response) {
      const responseData = await response.json();
      return responseData
    } else {
      throw new Error('Failed to verify 2FA');
    }
  } catch (error) {
    console.error("Unable to verify 2FA", error);
    throw error;
  }
}