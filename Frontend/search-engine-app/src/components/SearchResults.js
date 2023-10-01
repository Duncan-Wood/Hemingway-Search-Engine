import PropTypes from "prop-types";

// SearchResults component for displaying search results
const SearchResults = ({ results, resultCount, error, hasSearched, onReplace, onDelete, highlightQueryWord }) => (
  <div>
    {results.length > 0 ? (
      <>
        <p className="instances-count">
          {resultCount} instances found
        </p>
        <p className="results">Results</p>

        <div className="results-output">
          {error && <p>{error}</p>}
          {/* in the future,  I will adapt this to work with the similar search results as well */}
          {results.slice(0, 3).map((result, index) => (
            <div key={index}>
              {highlightQueryWord(`...${result.context}...`)}
            </div>
          ))}
        </div>
        <div className="menu-buttons">
          <button
            type="button"
            className="replace-button"
            onClick={onReplace}
          >
            <img
              src={require("../assets/replace.png")}
              alt="Menu Icon"
            />
          </button>
          <button
            type="button"
            className="menu-button"
            onClick={onDelete}
          >
            <img
              src={require("../assets/delete.png")}
              alt="Menu Icon"
            />
          </button>
        </div>
      </>
    ) : (
      hasSearched && (
        // Display "No results found" only if a search has been attempted
        <p className="noResults">No results found</p>
      )
    )}
  </div>
);

SearchResults.propTypes = {
  results: PropTypes.array.isRequired,
  resultCount: PropTypes.number.isRequired,
  error: PropTypes.string.isRequired,
  hasSearched: PropTypes.bool.isRequired,
  onReplace: PropTypes.func.isRequired,
  onDelete: PropTypes.func.isRequired,
  highlightQueryWord: PropTypes.func.isRequired,
};

export default SearchResults;
