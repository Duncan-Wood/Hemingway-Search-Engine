
// streamlined confirmation menu for replacing and deleting words

const Confirmation = ({
  isReplaceCompleted,
  showDeleteConfirmation,
  isDeleteCompleted,
  query,
  newWord,
  resultCount,
  confirmDelete,
}) => {
  if (isReplaceCompleted) {
    return (
      <div className="confirmation-menu">
        <p className="confirmation-text">
          All instances of "{query}" have been replaced with "{newWord}".
        </p>
      </div>
    );
  } else if (showDeleteConfirmation) {
    return (
      <div className="confirmation-menu">
        <p className="confirmation-text">
          Confirm deletion of {resultCount} instances of "{query}"?
        </p>
        <div className="menu-buttons confirmation">
          <button
            type="button"
            className="menu-buttons"
            onClick={confirmDelete} // Use the confirmDelete function
          >
            <img src={require("../assets/delete.png")} alt="Menu Icon" />
          </button>
        </div>
      </div>
    );
  } else if (isDeleteCompleted) {
    return (
      <div>
        <p className="confirmed-text">
          All instances of "{query}" have been deleted.
        </p>
      </div>
    );
  }
  return null; // No confirmation to render
};

export default Confirmation;
