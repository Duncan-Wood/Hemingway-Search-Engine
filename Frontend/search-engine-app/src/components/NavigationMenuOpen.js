// This component is used for displaying search results and actions

import { useState, useCallback } from "react";
import PropTypes from "prop-types";
import axios from "axios";
import "./NavigationMenuOpen.css";
import SearchResults from "./SearchResults";
import ReplaceSection from "./ReplaceSection";
import Confirmation from "./Confirmation";

// Constants
const API_BASE_URL = "http://localhost:5000";

// NavigationMenuOpen component for displaying search results and actions
const NavigationMenuOpen = ({ onClose }) => {
  // managing multiple state variables like this allows me to update them
  // individually without naming each one when updating
  const [state, setState] = useState({
    query: "", // The search query.
    results: [], // The search results.
    // will create a similarResults array to store similar words eventually
    resultCount: 0, // The number of results.
    error: "", // The error message.
    showResultsSection: true, // Flag to show/hide results section.
    newWord: "", // The new word to replace the query word.
    showReplaceSection: false, // Flag to show/hide replace section.
    isReplaceCompleted: false, // Flag to show/hide replace confirmation.
    showDeleteConfirmation: false, // Flag to show/hide delete confirmation.
    isDeleteCompleted: false, // Flag to show/hide delete confirmation.
    hasSearched: false, // Flag to indicate if a search has been attempted.
  });

  // Function to shuffle results array
  // this is an unnecessary function, but it's a way to show a diverse range of results
  const shuffleArray = (array) => {
    const shuffled = array.slice();
    for (let i = shuffled.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
    }
    return shuffled;
  };

// Function to highlight query words in text from results
// will eventually be used to highlight similar words by adding a similarResults array
const highlightQueryWord = (text) => {
  const { query } = state;
  const queryRegExp = new RegExp(`(${query.split(" ").map(escapeRegExp).join("|")})`, "gi");

  return text.split(queryRegExp).map((part, index) => {
    if (queryRegExp.test(part)) {
      return (
        <strong key={index}>
          {part}
        </strong>
      );
    }
    return part;
  });
};

// Function to escape special characters in a string for regex
const escapeRegExp = (str) => {
  // this is used to make the query case insensitive and ignore special characters
  return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
};


  const fetchSearchResults = useCallback(async () => {
    // useCallback is used to prevent the function from being recreated on every render
    try {
      const responseMatching = await axios.get(
        `${API_BASE_URL}/find_matching_sentences?input=${state.query}`
      );
      const matchingSentences = responseMatching.data.matching_sentences;
  
      if (matchingSentences.length >= 3) {
        // If we have at least three matching sentences, prioritize and shuffle them
        const randomized = shuffleArray(matchingSentences.slice(0, 3));
        setState((prevState) => ({
          ...prevState,
          results: randomized,
          resultCount: 3,
          error: "",
          hasSearched: true,
        }));
      } else {
        // Fetch similar words
        const similarWordsResponse = await axios.get(
          `${API_BASE_URL}/similar_words?w=${state.query}`
        );
  
        const similarWordsData = similarWordsResponse.data.similar_words.similar_words;
  
        if (Array.isArray(similarWordsData) && similarWordsData.length > 0) {
          // If we have similar words, fetch matching sentences for them
          const similarWords = similarWordsData.slice(0, 3);
          const similarWordsString = similarWords.join(',');
          const sentencesResponse = await axios.get(
            `${API_BASE_URL}/find_similar_sentences?similar_words=${similarWordsString}`
          );
          const similarSentences = sentencesResponse.data.matching_sentences;
    
          // Combine matching sentences and similar sentences, shuffle and select first three
          const combinedSentences = [...matchingSentences, ...similarSentences];
          const randomized = shuffleArray(combinedSentences.slice(0, 3));
  
          setState((prevState) => ({
            ...prevState,
            results: randomized,
            resultCount: 3,
            error: "",
            hasSearched: true,
          }));
        } else {
          // If there are no similar words, show an error message
          console.log('No similar words found.');
          setState((prevState) => ({
            ...prevState,
            results: [],
            resultCount: 0,
            error: "No matching or similar sentences found.",
            hasSearched: true,
          }));
        }
      }
    } catch (error) {
      console.error('Error fetching data:', error);
      handleSearchError(error);
    }
  }, [state.query]);

  const handleSearchError = (error) => {
    const errorMessage = error.response
      ? error.response.data.error
      : "An error occurred while fetching results.";

    setState((prevState) => ({
      ...prevState,
      error: errorMessage,
      results: [],
      resultCount: 0,
      hasSearched: true,
    }));
  };

  // Event handler for Enter key press to initiate search
  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      fetchSearchResults();
    }
  };

  // Function to handle word replacement
  const handleReplace = async () => {
    try {
      await axios.put(`${API_BASE_URL}/replace_word`, {
        old_word: state.query,
        new_word: state.newWord,
      });

      // Update UI or show a success message if needed
      setState({
        ...state,
        results: [],
        error: "",
        isDeleteCompleted: false,
        isReplaceCompleted: true,
        showResultsSection: false,
        showReplaceSection: false,
      });
    } catch (error) {
      handleReplaceError(error);
    }
  };

  const handleReplaceError = (error) => {
    const errorMessage = error.response
      ? error.response.data.error
      : "An error occurred while replacing the word.";

    setState({
      ...state,
      error: errorMessage,
    });
  };

  // Function to handle deletion confirmation
  const handleDelete = async () => {
    setState({
      ...state,
      showDeleteConfirmation: true,
    });
  };

  // Function to confirm and perform deletion
  const confirmDelete = async () => {
    try {
      await axios.delete(
        `${API_BASE_URL}/remove_similar_word?word=${state.query}`
      );

      // Update state after successful deletion
      setState({
        ...state,
        showDeleteConfirmation: false,
        results: [],
        error: "",
        isDeleteCompleted: true,
      });
    } catch (error) {
      // Handle errors and update state with an error message
      setState({
        ...state,
        error: error.response
          ? error.response.data.error
          : "An error occurred while deleting results.",
      });
    }
  };
  // Variables for readability
  const shouldShowResultsSection =
    state.showResultsSection &&
    !state.showDeleteConfirmation &&
    !state.isDeleteCompleted &&
    !state.isReplaceCompleted &&
    !state.showReplaceSection;

  const hasNoResults =
    state.hasSearched &&
    !state.showResultsSection &&
    !state.showDeleteConfirmation &&
    !state.isDeleteCompleted &&
    !state.isReplaceCompleted &&
    !state.showReplaceSection;

  return (
    <div className="menu menu-open">
      <div className="header" onClick={onClose}>
        <div className="menu-title">Menu</div>
        <div className="close-icon">
          <img src={require("../assets/x.png")} alt="Menu Icon" />
        </div>
      </div>
      <div className="input-section">
        <form>
          <label htmlFor="searchInput" className="searchLabel">
            Search
          </label>
          <input
            type="text"
            id="searchInput"
            className={state.query ? "input-filled" : ""}
            placeholder="Search text"
            value={state.query}
            onChange={(e) => setState({ ...state, query: e.target.value })}
            onKeyDown={handleKeyDown}
            disabled={
              state.showDeleteConfirmation ||
              state.isDeleteCompleted ||
              state.isReplaceCompleted
            }
          />

          {shouldShowResultsSection && (
            <SearchResults
              results={state.results}
              resultCount={state.resultCount}
              error={state.error}
              hasSearched={state.hasSearched}
              onReplace={() => {
                setState({
                  ...state,
                  showReplaceSection: true,
                  showResultsSection: false,
                });
              }}
              onDelete={handleDelete}
              highlightQueryWord={highlightQueryWord}
            />
          )}

          {hasNoResults && <p className="noResults">No results found</p>}

          {state.showReplaceSection && (
            <ReplaceSection
              newWord={state.newWord}
              handleReplace={handleReplace}
              handleNewWordChange={(e) =>
                setState({ ...state, newWord: e.target.value })
              }
            />
          )}

          <Confirmation
            showReplaceSection={state.showReplaceSection}
            isReplaceCompleted={state.isReplaceCompleted}
            showDeleteConfirmation={state.showDeleteConfirmation}
            isDeleteCompleted={state.isDeleteCompleted}
            query={state.query}
            newWord={state.newWord}
            resultCount={state.resultCount}
            confirmDelete={confirmDelete}
          />
        </form>
      </div>
    </div>
  );
};

// he onClose prop must be a required function
NavigationMenuOpen.propTypes = {
  onClose: PropTypes.func.isRequired,
};

export default NavigationMenuOpen;
