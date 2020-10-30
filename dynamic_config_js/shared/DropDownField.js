import React from "react";
import PropTypes from "prop-types";
import { capitalize } from "../../utils";
import Form from "react-bootstrap/Form";

const DropDownField = ({
  name,
  label,
  onChange,
  defaultOption,
  value,
  error,
  options,
}) => {
  return (
    <Form.Group controlId={name}>
      <Form.Label>{label}</Form.Label>
      <Form.Control
        as="select"
        name={name}
        value={value}
        onChange={onChange}
        defaultValue={defaultOption}
      >
        <option value="">-- Select {label} --</option>
        {options.map((option) => {
          return (
            <option key={option} value={option}>
              {capitalize(option)}
            </option>
          );
        })}

        {
          //TODO: taost an error
          error && <div className="alert alert-danger">{error}</div>
        }
      </Form.Control>
    </Form.Group>
  );
};

DropDownField.propTypes = {
  name: PropTypes.string.isRequired,
  label: PropTypes.string.isRequired,
  onChange: PropTypes.func.isRequired,
  defaultOption: PropTypes.string,
  value: PropTypes.string,
  error: PropTypes.string,
  options: PropTypes.array,
};

export default DropDownField;
