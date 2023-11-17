import React, { useState } from "react";
import "../css/ProductForm.css"; // Import the CSS file

function ProductForm({
  product,
  isProductPictureRequired,
  handleInputChange,
  handleProductPictureChange,
  handleSubmit,
}) {

  return (
    <form className="create-account-form" onSubmit={handleSubmit}>
      <div className="form-group">
        <label htmlFor="name">Name of Product:</label>
        <input
          type="text"
          placeholder="Enter name of product"
          name="ProductName"
          value={product.ProductName}
          onChange={handleInputChange}
          className="form-control"
          required
        />
      </div>
      <div className="form-group">
        <label htmlFor="quantity">Quantity:</label>
        <input
          type="number"
          placeholder="Enter product Quantity"
          name="quantity"
          value={product.quantity}
          onChange={handleInputChange}
          required
          className="form-control"
          title="Please quantity needs to be greater than 1"
        />
      </div>
      <div className="form-group">
        <label htmlFor="cost">Cost ($):</label>
        <input
          type="number"
          placeholder="Enter Product Cost"
          name="cost"
          value={product.cost}
          onChange={handleInputChange}
          required
          min="0.10"
          step="0.01"
          className="form-control"
          title="Please enter the cost of the product (at least $0.10)"
        />
      </div>
      <div className="form-group">
        <label htmlFor="ProductPicture">Upload Product Picture:</label>
        <input
          type="file"
          name="ProductPicture"
          id="ProductPicture"
          accept="image/*"
          onChange={handleProductPictureChange}
          className="form-control"
          {...(isProductPictureRequired && { required: true })}
          title="Please upload an image for the product (JPG or PNG)"
        />
      </div>
      <div className="form-group">
        <label htmlFor="description">Description:</label>
        <textarea
          name="description"
          placeholder="Max 300 characters"
          pattern="[\s\S]{0,300}"
          value={product.description}
          onChange={handleInputChange}
          required
          className="form-control"
          title="Please enter a description of the product"
        ></textarea>
      </div>
      <div className="form-group">
        <label>Product Type:</label>
        <select
          name="productType"
          value={product.productType}
          onChange={handleInputChange}
          className="form-control"
        >
          <option value="sports">Sports</option>
          <option value="leisure">Leisure</option>
          <option value="computer">Computer</option>
        </select>
      </div>
      <div className="form-group">
        <label>Availability:</label>
        <select
          name="status"
          value={product.availability}
          onChange={handleInputChange}
          className="form-control"
        >
          <option value="In Stock">In Stock</option>
          <option value="Out of Stock">Out of Stock</option>
        </select>
      </div>
      <button type="submit" className="submit-button">
        Submit
      </button>
    </form>
  );
  
}

export default ProductForm;
