import React, { useEffect, useRef } from "react";
import "../css/productModal.css"; // Import the CSS file

function ProductDescription({ product, onClose, recommendations }) {
  const modalRef = useRef(null);
  // Add a click event listener to the background overlay
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (modalRef.current && !modalRef.current.contains(event.target)) {
        onClose(); // Call the onClose function if a click occurs outside the modal
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [onClose]);

  // Check if the product is null before rendering
  if (!product) {
    return null;
  }

  return (
    <div className="product-modal" onClick={onClose}>
      <div className="product-modal-content" onClick={(e) => e.stopPropagation()}>
        <button className="close-button" onClick={onClose}>
          &times;
        </button>
        <div className="product-details">
          <div className="product-image">
            <img src={product.ProductPicture} alt={product.ProductName} />
          </div>
          <div className="product-info">
            <h2 className="product-name">{product.ProductName}</h2>
            <p className="product-description">{product.description}</p>
            <p className="product-quantity">Quantity: {product.quantity}</p>
            <p className="product-type">Product Type: {product.productType}</p>
            <p className="product-status">Status: {product.status}</p>
          </div>
          <div id="productCards">
          </div>
          {recommendations !== null &&
            recommendations.slice(0, 3).map((recommendation) => {
            const card = document.createElement("div");
            card.className = "card";
            card.style.display = "inline-block";
            card.innerHTML = `
                <h3>${recommendation.ProductName}</h3>
                <img src="${recommendation.ProductPicture}" alt="${recommendation.ProductName}">
                <p>Cost: ${recommendation.cost}</p>
            `;
            const productCardsContainer = document.getElementById("productCards");
            if (productCardsContainer) {
              productCardsContainer.appendChild(card);
            } else {
              // If the container doesn't exist, you can create it or handle it as needed.
            }

            })
          }
        </div>
        
      </div>
    </div>
  );
}
export default ProductDescription;
