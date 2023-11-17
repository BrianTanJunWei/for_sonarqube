import React from "react";

function FilterMenuLeft({ brands, checkedBoxes, handleCheckboxChange, getAllCheckedBoxes }) {
  const handleCheckboxChangeLocal = (event) => {
    const value = event.target.value;
    const isChecked = event.target.checked;

    handleCheckboxChange(value, isChecked);
  }

  return (
    <ul className="list-group list-group-flush rounded">
      <li className="list-group-item">
        <h5 className="mt-1 mb-1">Brands</h5>
        <div className="d-flex flex-column">
          {brands.map((v, i) => (
            <div key={i} className="form-check">
              <input
                className="form-check-input"
                type="checkbox"
                value={v}
                checked={checkedBoxes[v]}
                onChange={handleCheckboxChangeLocal}
              />
              <label className="form-check-label" htmlFor={`checkbox-${i}`}>
                {v}
              </label>
            </div>
          ))}
        </div>
      </li>
      <li className="list-group-item">
        <button className="btn btn-primary" onClick={getAllCheckedBoxes}>
          Get Checked Boxes
        </button>
      </li>
    </ul>
  );
}

export default FilterMenuLeft;
