import React, { useState, useEffect } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import ScrollToTopOnMount from "../Components/ScrollToTopOnMount";
import AdminSidePanel from "../Components/AdminSidePanel";
import ProductList from "../Components/ProductList"; // Import the ProductList component
import { fetchAllProducts } from "../services/Services";

function AdminView() {
  const [viewType, setViewType] = useState({ grid: true });
  const [products, setProducts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  function changeViewType() {
    setViewType({
      grid: !viewType.grid,
    });
  }

  useEffect(() => {
    // Fetch products data from the API service
    fetchAllProducts()
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

  return (
    <div className="container-fluid">
      <ScrollToTopOnMount />

      <div className="row mb-4 mt-lg-3">
        <div className="col-lg-3">
          <AdminSidePanel />
        </div>

        <div className="col-lg-9">
          <nav aria-label="breadcrumb" className="bg-custom-light rounded">
            <ol className="breadcrumb p-3 mb-0">
              <li className="breadcrumb-item">All Products</li>
            </ol>
          </nav>

          <div className="d-flex flex-column h-100">
            <div className="row mb-3">
              <div className="col-lg-3 d-none d-lg-block"></div>
              <div className="col-lg-9 col-xl-5 offset-xl-4 d-flex flex-row">
                <div className="input-group">
                  <input
                    className="form-control"
                    type="text"
                    placeholder="Search products..."
                    aria-label="search input"
                  />
                  <button className="btn btn-outline-dark">
                    <FontAwesomeIcon icon={["fas", "search"]} />
                  </button>
                </div>
                <button
                  className="btn btn-outlineDark ms-2 d-none d-lg-inline"
                  onClick={changeViewType}
                >
                  <FontAwesomeIcon
                    icon={["fas", viewType.grid ? "th-list" : "th-large"]}
                  />
                </button>
              </div>
            </div>
            <ProductList products={products} viewType={viewType} />
            <div className="d-flex align-items-center mt-auto"></div>
          </div>
        </div>
      </div>
    </div>
  );

}

export default AdminView;
