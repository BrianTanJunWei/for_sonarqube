    // ProductList component to render the list of products
    import React from "react";
    import { ProductCard } from "./ProductCard";
    import AddToCartButton from "./AddToCart"; // Import the AddToCart component

    export function ProductList({ products, viewType }) {
        return (
        <div
            className={`row row-cols-1 row-cols-md-2 row-cols-lg-2 g-3 mb-4 flex-shrink-0 ${
            viewType.grid ? "row-cols-xl-3" : "row-cols-xl-2"
            }`}
        >
            {products.map((product, index) => (
            <ProductCard key={index} product={product} />
            ))}
        </div>
        );
    }

    export function MainProductList({ products, viewType, openModal, addToCart, isSellerView }) {
        const handleButtonClick = (e, product) => {
          // Prevent the click event from propagating to the parent elements
          e.stopPropagation();
          addToCart(product);
        };
      
        return (
            <div
              className={`row row-cols-1 row-cols-md-2 row-cols-lg-2 g-3 mb-4 flex-shrink-0 ${
                viewType.grid ? "row-cols-xl-3" : "row-cols-xl-2"
              }`}
            >
              {products.map((product, index) => (
                <div key={index}>
                  <div className="card" onClick={() => openModal(product)}>
                    <h5 className="card-title">{product.ProductName}</h5>
                    <img src={product.ProductPicture} className="card-img-top" alt={product.ProductName} />
                    <div className="card-body">
                      <p className="card-text">Cost: ${product.cost}</p>
                    </div>
                  </div>
                  {!isSellerView && ( // Conditionally render the "Add to Cart" button except in SellerView
                    <div class="cartAdd">
                      <AddToCartButton
                        item={{
                          id: product.ProductID,
                          name: product.ProductName,
                          price: product.cost,
                        }}
                        // fetchCartData = {fetchCartData}
                        onAddToCart={() => handleButtonClick(product)}
                      />
                    </div>
                  )}
                </div>
              ))}
            </div>
          );
      }
      
      

    export default ProductList