// src/pages/AddProducts.js
import React,{ useState, useEffect } from "react";
import ProductForm from "../Components/ProductForm";
import { addProduct } from "../services/Services";
import Cookies from "js-cookie";
import { jwtDecode } from "jwt-decode";
import { verifySession } from "../Components/Sessionvalidation";

function AddProducts() {
  useEffect(() => {
    verifySession();
  }, []);
  
  const [ProductPicture, setProductPicture] = useState(null);

  let sellerUID = '';
  // Setting Cookies up
  const cookieSession = Cookies.get('session');
  if (cookieSession){
    const sessionCookie = jwtDecode(cookieSession, { header: true });
    sellerUID = sessionCookie.user_id;
  }
  // Define the generateRandomProductID function
  function generateRandomProductID() {
    // Generate a random number and convert it to a string
    const randomNum = Math.floor(Math.random() * 1000000).toString();

    // Add a prefix to make it unique (you can modify the prefix as needed)
    const prefix = "PROD";

    // Combine the prefix and random number to create the product ID
    const productID = prefix + randomNum;

    return productID;
  }

  const [product, setProduct] = useState({
    name: "",
    pid: generateRandomProductID(), // Generate a unique product ID
    quantity: 1, // Default quantity to 1
    cost: 0, // Default cost to 0
    imageURL: "",
    description: "",
    productType: "sports",
    availability: "In Stock", // Default status to "In Stock"
  });

  const handleProductPictureChange = (e) => {
    const selectedFile = e.target.files[0];
    setProductPicture(selectedFile);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setProduct({
      ...product,
      [name]: value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
 
    if (ProductPicture === null) {
      alert("Please upload a product picture!");
      return;
    }
  
    const ProductData = new FormData();
    ProductData.append('ProductName', product.ProductName);
    ProductData.append('PID', product.pid);
  
    if (product.quantity < 1) {
      alert("Quantity must be greater than 1.");
      return;
    } else {
      ProductData.append('quantity', product.quantity);
    }
  
    ProductData.append('cost', product.cost);
  
    // Append the product picture only if it's not null
    ProductData.append('ProductPicture', ProductPicture);
  
    ProductData.append('description', product.description);
    ProductData.append('productType', product.productType);
    ProductData.append('sellerUID', sellerUID);
    ProductData.append('status', product.availability);
    handleProductSubmit(ProductData);
  };

  const handleProductSubmit = async (productData) => {
    try {
      const response = await addProduct(productData);
  
      if (response) {
        // Display a success alert
        window.alert("Product added successfully");
        window.location.href = '/SellerProducts';
        // Optionally, you can redirect the user to a different page here.
      } else {
        // Display an error alert
        window.alert("Product failed to add");
      }
    } catch (error) {
      // Display an error alert for any exceptions
      console.log("Error during Product registration: " + error.message);
    }
  };
  

  return (
    <div className="create-account-container">
      <h2>Add Product</h2>
      <ProductForm
        onProductSubmit={handleProductSubmit}
        product={product}
        isProductPictureRequired={true}
        handleInputChange={handleInputChange}
        handleProductPictureChange={handleProductPictureChange}
        handleSubmit={handleSubmit}
      />
    </div>
  );
}

export default AddProducts;
