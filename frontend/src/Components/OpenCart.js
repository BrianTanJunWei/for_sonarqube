import React from 'react';
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

const OpenCartButton = ({ onClick }) => {
  return (
    <button onClick={onClick} type="button" className="btn btn-outline-dark me-3 d-none d-lg-inline">
      <FontAwesomeIcon icon={["fas", "shopping-cart"]} />
      {/* <span className="ms-3 badge rounded-pill bg-dark">0</span> */}
    </button>
  );
};

export default OpenCartButton;
