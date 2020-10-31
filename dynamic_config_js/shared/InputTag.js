import React from "react";
import PropTypes from "prop-types";
import "./InputTag.css";

const InputTag = ({ label, name, placeHolder, value, onChange }) => {
  const tags = value;
  let tagInput = null;

  const removeTag = (i) => {
    let newTags = [...tags];
    newTags.splice(i, 1);

    onChange({ target: { value: newTags.length > 0 ? [newTags] : [], name } });
  };

  const inputKeyDown = (e) => {
    const val = e.target.value;
    if (e.key === "Enter" && val) {
      if (tags.find((tag) => tag.toLowerCase() === val.toLowerCase())) {
        return;
      }
      tagInput.value = null;
      onChange({ target: { value: [...tags, val], name } });
    } else if (e.key === "Backspace" && !val) {
      removeTag(tags.length - 1);
    }
  };

  return (
    <div className="form-group wrapper">
      <label htmlFor={name}>{label}</label>
      <div className="input-tag">
        <ul name={name} className="input-tag__tags">
          {tags.map((tag, i) => (
            <li key={tag}>
              {tag}
              <button
                type="button"
                onClick={() => {
                  removeTag(i);
                }}
              >
                +
              </button>
            </li>
          ))}
          <li className="input-tag__tags__input">
            <input
              type="text"
              placeholder={placeHolder}
              onKeyDown={inputKeyDown}
              ref={(c) => {
                tagInput = c;
              }}
            />
          </li>
        </ul>
      </div>
    </div>
  );
};

InputTag.propTypes = {
  label: PropTypes.string.isRequired,
  name: PropTypes.string.isRequired,
  placeHolder: PropTypes.string,
  value: PropTypes.array.isRequired,
  onChange: PropTypes.func.isRequired,
};

export default InputTag;
