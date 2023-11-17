// ProductCard component to render a single product card
export function ProductCard({ product }) {
    return (
      <div className="col">
        <div className="card">
          <h5 className="card-title">{product.ProductName}</h5>
          <img src={product.ProductPicture} alt="" className="card-img-top" />
          <div className="card-body">
            <p className="card-text">Cost: ${product.cost}</p>
          </div>
        </div>
      </div>
    );
  }

 export function SellerProductCard({ product, editProduct, deleteProduct }) {
    return (
      <div className="col-md-4">
        <div className="card text-center">
          <h5 className="card-title mb-3">{product.ProductName}</h5>
          <hr className="mx-3" />
          <div className="card-body">
            <img
              src={product.ProductPicture}
              className="card-img-top mx-auto"
              alt={product.ProductName}
            />
            <hr className="my-3" />
            <p className="card-text">Cost: ${product.cost}</p>
            <button className="btn btn-primary me-2" onClick={() => editProduct(product.ProductID)}>
              Edit
            </button>
            <button className="btn btn-danger" onClick={() => deleteProduct(product.ProductID)}>
              Delete
            </button>
          </div>
        </div>
      </div>
    );
  }
