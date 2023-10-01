import React from "react";
import PropTypes from "prop-types";

const ReplaceSection = ({
  newWord,
  handleReplace,
  handleNewWordChange,
}) => {
  return (
    <div className="replace-section">
      <label htmlFor="newWordInput" className="searchLabel">
        Replace with
      </label>
      <div className="replace-input">
        <input
          type="text"
          id="newWordInput"
          className={newWord ? "input-filled" : ""}
          placeholder="New word"
          value={newWord}
          onChange={handleNewWordChange}
        />
        <div className="replace-container">
          <button type="button" className="replace-button" onClick={handleReplace}>
            <img src={require("../assets/replace-confirm.png")} alt="Menu Icon" />
          </button>
        </div>
      </div>
      <p className="warning">This cannot be reversed!</p>
    </div>
  );
};

ReplaceSection.propTypes = {
  newWord: PropTypes.string.isRequired,
  showReplaceSection: PropTypes.bool.isRequired,
  isReplaceCompleted: PropTypes.bool.isRequired,
  handleReplace: PropTypes.func.isRequired,
  handleNewWordChange: PropTypes.func.isRequired,
};

export default ReplaceSection;
