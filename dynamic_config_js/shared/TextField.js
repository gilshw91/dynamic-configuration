import React from "react";
import PropTypes from "prop-types";

const TextField = ({
  name,
  label,
  type,
  placeholder,
  value,
  error,
  onChange,
}) => {
  let wrapperClass = "form-group";
  if (error && error.length > 0) {
    wrapperClass += ` has-error`;
  }

  return (
    <div className={wrapperClass}>
      <label htmlFor={name}>{label}</label>
      <div className="field">
        <input
          type={type}
          name={name}
          className="form-control"
          placeholder={placeholder}
          value={value}
          onChange={onChange}
        />
        {error && <div className="alert alert-danger">{error}</div>}
      </div>
    </div>
  );
};

TextField.defaultProps = {
  type: "text",
};

TextField.propTypes = {
  name: PropTypes.string.isRequired,
  label: PropTypes.string.isRequired,
  type: PropTypes.string,
  placeholder: PropTypes.string,
  value: PropTypes.string,
  error: PropTypes.string,
  onChange: PropTypes.func.isRequired,
};

export default TextField;
