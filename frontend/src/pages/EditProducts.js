import React, { useState, useEffect, useMemo } from "react";
import { useLocation, useNavigate } from 'react-router-dom';
import ProductForm from "../Components/ProductForm";
import { fetchProductData, updateProduct } from "../services/Services";
import Cookies from "js-cookie";
import { jwtDecode } from "jwt-decode";

function EditProduct() {
  const location = useLocation();
  const [ProductPicture, setProductPicture] = useState(null);
  let UserID = '';
  // Setting Cookies up
  const cookieSession = Cookies.get('session');
  if (cookieSession){
    const sessionCookie = jwtDecode(cookieSession, { header: true });
    UserID = sessionCookie.user_id;
  }
  const navigate = useNavigate();

  const productId = useMemo(() => location.state?.productId || { productId }, [
    location.state?.productId,
  ]);

  const [product, setProduct] = useState({
    ProductName: "",
    quantity: 1,
    cost: 0,
    ProductPicture: "",
    description: "",
    productType: "sport",
    availability: "In Stock",
  });
  

  useEffect(() => {
    async function fetchData() {
      const data = await fetchProductData(productId, UserID);
      if (data) {
        setProduct(data);
      } else {
        console.error("Product not found.");
      }
    }

    fetchData();
  }, [UserID, productId]);

  const isProductPictureRequired = !product.ProductPicture;

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setProduct({
      ...product,
      [name]: value,
    });
  };

  const handleProductPictureChange = (e) => {
    const selectedFile = e.target.files[0];
    setProductPicture(selectedFile);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const ProductData = new FormData();
    ProductData.append("ProductName", product.ProductName);
    ProductData.append("quantity", product.quantity);
    ProductData.append("cost", product.cost);

    // Only append a new image if one is selected
    if (ProductPicture) {
      ProductData.append("ProductPicture", ProductPicture);
    }

    ProductData.append("description", product.description);
    ProductData.append("productType", product.productType);
    ProductData.append("availability", product.availability);

    try {
      await updateProduct(productId, ProductData);
      window.alert("Product Update Successful!")
      navigate("/SellerProducts");
    } catch (error) {
      window.alert("Error Updating product. Please try again!")
      console.error("Error updating products:", error);
    }
  };

  return (
    <ProductForm
      product={product}
      isProductPictureRequired={isProductPictureRequired}
      handleInputChange={handleInputChange}
      handleProductPictureChange={handleProductPictureChange}
      handleSubmit={handleSubmit}
    />
  );
}

export default EditProduct;
