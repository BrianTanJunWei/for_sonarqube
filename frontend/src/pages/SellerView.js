import React, { useState, useEffect } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import ScrollToTopOnMount from "../Components/ScrollToTopOnMount";
import ProductDescription from "../Components/ProductDescription"; // Import your ProductDescription component
import { MainProductList } from "../Components/ProductList";
import { verifySession } from "../Components/Sessionvalidation";


function SellerView() {
  const [products, setProducts] = useState([]);
  const [viewType, setViewType] = useState({ grid: true });
  const [isLoading, setIsLoading] = useState(true);
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  function changeViewType() {
    setViewType({
      grid: !viewType.grid,
    });
  }

  useEffect(() => {
    verifySession();
    // Fetch products data based on the Seller's UID from the Flask backend
    fetch("/FetchAllProducts")
      .then((response) => response.json())
      .then((data) => {
        if (data.length > 0) {
          setProducts(data);
        }
        setIsLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching products:", error);
        setIsLoading(false);
      });
  }, []);

  // Function to open the modal with a product
  const openModal = (product) => {
    setSelectedProduct(product);
    setIsModalOpen(true);
  };

  // Function to close the modal
  const closeModal = () => {
    setSelectedProduct(null);
    setIsModalOpen(false);
  };

  return (
    <div className="container mt-5 py-4 px-xl-5">
      <ScrollToTopOnMount />
      <nav aria-label="breadcrumb" className="bg-custom-light rounded">
        <ol className="breadcrumb p-3 mb-0">
          <li className="breadcrumb-item">All Products</li>
        </ol>
      </nav>

      <div className="h-scroller d-block d-lg-none">
        <nav className="nav h-underline">
          {/* Add navigation links if needed */}
        </nav>
      </div>

      <div className="row mb-4 mt-lg-3 justify-content-center">
        <div className="d-none d-lg-block col-lg-3"></div>
        <div className="col-lg-9">
          <div className="d-flex flex-column h-100">
            <div className="row mb-3">
              <div className="col-lg-9 col-xl-5 offset-xl-4 d-flex flex-row">
                <button
                  className="btn btn-outline-dark ms-2 d-none d-lg-inline"
                  onClick={changeViewType}
                >
                  <FontAwesomeIcon
                    icon={["fas", viewType.grid ? "th-list" : "th-large"]}
                  />
                </button>
              </div>
            </div>
             {/* Use the MainProductList component here and pass the required props */}
             <MainProductList
        products={products}
        viewType={viewType}
        openModal={openModal}
        isSellerView={true} // Set isSellerView to true
      />
            <div className="d-flex align-items-center mt-auto">
              {/* Navigation buttons */}
            </div>
          </div>
        </div>
      </div>

      {/* Product Description Modal */}
      {isModalOpen && (
        <ProductDescription
          product={selectedProduct}
          onClose={closeModal}
        />
      )}
    </div>
  );
}

export default SellerView;
