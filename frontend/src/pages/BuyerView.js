import { Link } from "react-router-dom";
import React, { useState, useEffect } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import ScrollToTopOnMount from "../Components/ScrollToTopOnMount";
import ProductDescription from "../Components/ProductDescription";
import AddToCartButton from "../Components/AddToCart";
import { fetchAllProducts, fetchFilteredProducts } from "../services/Services";
import FilterMenuLeft from "../Components/FilterMenuLeft";
import ProductList, { MainProductList } from "../Components/ProductList";
import { verifySession } from "../Components/Sessionvalidation";

const categories = ["All Products"];

function BuyerView() {
  const [brands, setBrands] = useState([]);
  const [products, setProducts] = useState([]);
  const [viewType, setViewType] = useState({ grid: true });
  const [checkedBoxes, setCheckedBoxes] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchProducts, setSearchProducts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [recommendations, setRecommendations] = useState(null);

  const openModal = (product) => {
    setSelectedProduct(product);
    const recommendationsFilter = {}
    recommendationsFilter[product.productType] = "0"
    fetchFilteredProducts(recommendationsFilter)
      .then((data) => {
        setRecommendations(data);
      })
      .catch((error) => {
        console.error('Error fetching recommendations: ', error);
      });
    setIsModalOpen(true);
  };

  

  const closeModal = () => {
    setSelectedProduct(null);
    setIsModalOpen(false);
  };

  const handleSearch = () => {
    const filteredProducts = products.filter((product) =>
      product.ProductName.includes(searchQuery)
    );

    setSearchProducts(filteredProducts);
  };
  async function getAllCheckedBoxes() {
    const updatedProductList = await fetchFilteredProducts(checkedBoxes);
    setProducts(updatedProductList);
  }
  const changeViewType = () => {
    setViewType({
      grid: !viewType.grid,
    });
  };

  useEffect(() => {
    verifySession();
    fetchAllProducts()
      .then((data) => {
        if (data.length > 0) {
          setProducts(data);
          const uniqueBrands = [...new Set(data.map((product) => product.productType))];
          setBrands(uniqueBrands);
        }
        setIsLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching products:", error);
        setIsLoading(false);
      });
  }, []);

  
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
          {categories.map((v, i) => (
            <div key={i} className="h-link me-2">
              <Link
                to="/products"
                className="btn btn-sm btn-outline-dark rounded-pill"
                replace
              >
                {v}
              </Link>
            </div>
          ))}
        </nav>
      </div>

      <div className="row mb-3 d-block d-lg-none">
        <div className="col-12">
          <div id="accordionFilter" className="accordion shadow-sm">
            <div className="accordion-item">
              <h2 className="accordion-header" id="headingOne">
                <button
                  className="accordion-button fw-bold collapsed"
                  type="button"
                  data-bs-toggle="collapse"
                  data-bs-target="#collapseFilter"
                  aria-expanded="false"
                  aria-controls="collapseFilter"
                >
                  Filter Products
                </button>
              </h2>
            </div>
            <div
              id="collapseFilter"
              className="accordion-collapse collapse"
              data-bs-parent="#accordionFilter"
            >
              <div className="accordion-body p-0">
                <FilterMenuLeft
                  brands={brands}
                  checkedBoxes={checkedBoxes}
                  handleCheckboxChange={(value, isChecked) => {
                    setCheckedBoxes((prevCheckedBoxes) => ({
                      ...prevCheckedBoxes,
                      [value]: isChecked,
                    }));
                  }}
                  getAllCheckedBoxes={getAllCheckedBoxes}
                />
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="row mb-4 mt-lg-3 justify-content-center">
        <div className="d-none d-lg-block col-lg-3">
          <div className="border rounded shadow-sm">
            <FilterMenuLeft
              brands={brands}
              checkedBoxes={checkedBoxes}
              handleCheckboxChange={(value, isChecked) => {
                setCheckedBoxes((prevCheckedBoxes) => ({
                  ...prevCheckedBoxes,
                  [value]: isChecked,
                }));
              }}
              getAllCheckedBoxes={getAllCheckedBoxes}
            />
          </div>
        </div>
        <div className="col-lg-9">
          <div className="d-flex flex-column h-100">
            <div className="row mb-3">
              <div className="col-lg-3 d-none d-lg-block">
                <select
                  className="form-select"
                  aria-label="Default select example"
                  defaultValue=""
                >
                  <option value="">All Models</option>
                  <option value="1">iPhone X</option>
                  <option value="2">iPhone Xs</option>
                  <option value="3">iPhone 11</option>
                </select>
              </div>
              <div className="col-lg-9 col-xl-5 offset-xl-4 d-flex flex-row">
                <div className="input-group">
                  <input
                    className="form-control"
                    type="text"
                    placeholder="Search products..."
                    aria-label="search input"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                  />
                  <button onClick={handleSearch} className="btn btn-outline-dark">
                    <FontAwesomeIcon icon={["fas", "search"]} />
                  </button>
                </div>
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

            <MainProductList
              products={
                searchProducts.length !== 0 ? searchProducts : products
              }
              viewType={viewType}
              openModal={openModal}
              addToCart={(product) => {
                // Add to cart logic here
                console.log(`Added to cart: ${product.ProductName}`);
              }}
            />

            <div className="d-flex align-items-center mt-auto"></div>
          </div>
        </div>
      </div>

      {isModalOpen && (
        <ProductDescription product={selectedProduct} recommendations={recommendations} onClose={closeModal} />
      )}
    </div>
  );

}

export default BuyerView;
