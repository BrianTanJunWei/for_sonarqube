import React, { useState, useEffect, navigate} from "react";
import { Link, useNavigate  } from "react-router-dom"; // Import Link and useHistory
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import ScrollToTopOnMount from "../Components/ScrollToTopOnMount";
import "../css/sellerProducts.css"; // Import the CSS file
import { SellerProductCard } from "../Components/ProductCard";
import { fetchSellerProducts, deleteProduct } from "../services/Services";
import Cookies from "js-cookie";
import { jwtDecode } from "jwt-decode";
import { verifySession } from "../Components/Sessionvalidation";

function SellerProducts() {
  const [products, setProducts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    verifySession();
    async function fetchData() {
      let userId = '';
      try {
      // Setting Cookies up
      const cookieSession = Cookies.get('session');
      if (cookieSession){
        const sessionCookie = jwtDecode(cookieSession, { header: true });
        userId = sessionCookie.user_id;
      }
        const data = await fetchSellerProducts(userId);
        if (data.length > 0) {
          setProducts(data);
        }
        setIsLoading(false);
      } catch (error) {
        // Handle error appropriately
        setIsLoading(false);
      }
    }

    fetchData();
  }, []);

   // Function to delete a product by ID
const handleDeleteProduct = async (productId) => {
  const isDeleted = await deleteProduct(productId);

  if (isDeleted) {
    // Product deleted successfully, update the products state
    const updatedProducts = products.filter(
      (product) => product.ProductID !== productId
    );
    setProducts(updatedProducts);
    window.alert("Product Successfully deleted");
  }
};

  // Function to edit a product by ID
  const editProduct = (productId) => {
    // Set the selected productId in state
    navigate('/EditProducts', { state: { productId } });
  };

  function renderProducts() {
    if (isLoading) {
      return <p>Loading...</p>;
    }

    if (products.length === 0) {
      return <p>You do not have any products.</p>;
    }

    return (
      <div className="row">
      {products.map((product) => (
        <SellerProductCard
          key={product.ProductID}
          product={product}
          editProduct={editProduct}
          deleteProduct={handleDeleteProduct}
        />
      ))}
    </div>

    );    
  }

  return (
    <div className="container mt-5 py-4 px-xl-5">
      <ScrollToTopOnMount />
      <nav aria-label="breadcrumb" className="bg-custom-light rounded">
        <ol className="breadcrumb p-3 mb-0">
          <li className="breadcrumb-item">All Products</li>
        </ol>
      </nav>

      <div className="h-scroller d-block d-lg-none">
        <nav className="nav h-underline"></nav>
      </div>

      {/* Render products or message */}
      {renderProducts()}

      {/* Add products button */}
      <div className="text-center mt-4">
        <Link to="/AddProducts" className="btn btn-primary">
          Add Products
        </Link>
      </div>
    </div>
  );
}

export default SellerProducts;
