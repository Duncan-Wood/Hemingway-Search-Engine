# ./index.py
"""Search Engine API"""

import re # used for regular expressions
import logging # used to log errors
import pickle # used to load the custom vocabulary
from flask import Flask, jsonify, request # used to create the API
from flask_cors import CORS # used to enable Cross-Origin Resource Sharing
from .word2vec_utils import find_most_similar_words # used to find similar words
from .config import CORPUS_FILE_PATH, CONTEXT_SIZE, ERROR_MESSAGES # used to load the corpus file path, context size, and error messages

# Create a Flask app and enable CORS
app = Flask(__name__)
CORS(app)

# Helper function for file operations
def file_operation(file_path, operation, data=None, encoding='utf-8'):
    """
    Helper function for file operations.

    file_path: The path to the file.
    operation: The operation to perform ('read' or 'write').
    data: Data to write to the file (only used for 'write' operation).
    encoding: The encoding for file operations.
    return: Success message or error message.
    """
    try:
        if operation == 'read':
            with open(file_path, 'r', encoding=encoding) as file:
                return file.read()
        elif operation == 'write':
            with open(file_path, 'w', encoding=encoding) as file:
                file.write(data)
            return "write successful"
    except FileNotFoundError as exc:
        logging.error("Error in file operation: %s", exc)
        raise FileNotFoundError("Text file not found") from exc
    except Exception as exc: # pylint: disable=W0718
        logging.error("Error in file operation: %s", exc)
        return "exception occurred"
    return None

# Load the corpus from a text file
def load_corpus(file_path):
    """
    Load the corpus from a text file.

    file_path: The path to the corpus file.
    return: List of words from the corpus.
    """
    try:
        corpus_text = file_operation(file_path, 'read')
        # Use regular expression to split corpus_text into words
        # This pattern splits text by spaces or punctuation, while preserving words with punctuation
        words = re.findall(r'\b\w+\b|[\.,!?;]', corpus_text)
        return words
    except FileNotFoundError as exc:
        raise exc


# Save the corpus to a text file
def save_corpus(file_path, new_word_list, encoding='utf-8'):
    """
    Save the corpus to a text file.

    file_path: The path to the corpus file.
    new_word_list: List of words to save to the file.
    encoding: The encoding for file operations.
    return: The saved word list.
    """
    try:
        file_operation(file_path, 'write', ' '.join(new_word_list), encoding=encoding)
        return new_word_list
    except FileNotFoundError as exc:
        raise exc

# Load the initial word list from the corpus file
word_list = load_corpus(CORPUS_FILE_PATH)

# Load the custom vocabulary from the pickle file
with open('vocabulary.pkl', 'rb') as vocab_file:
    custom_vocab = pickle.load(vocab_file)

# Common function to find matching sentences for a word
def find_matching_sentences_for_word(input_word):
    """This is a common function to find matching sentences for a word"""
    try:
        # Validate input_word using the input validation function
        validation_error = validate_input_string(input_word, 'input word')
        if validation_error:
            raise ValueError(validation_error)

        with open(CORPUS_FILE_PATH, 'r', encoding='utf-8') as file:
            hemingway = file.read()

        sentences = re.split(r'(?<=[.!?])\s+', hemingway)
        matching_sentences = []

        for sentence in sentences:
            if re.search(rf'\b{input_word}\b', sentence, re.IGNORECASE):
                match_index = sentence.lower().index(input_word.lower())
                context_start = max(match_index - CONTEXT_SIZE, 0)
                context_end = min(match_index + len(input_word) + CONTEXT_SIZE, len(sentence))
                context = sentence[context_start:context_end]
                context = context.replace("\n", " ").strip()
                matching_sentences.append({"context": context})

        return matching_sentences

    except Exception as exc: # pylint: disable=W0718
        logging.warning("Error processing request: %s", exc)
        return []

# Define a reusable input validation function
def validate_input_string(input_value, field_name):
    """
    Validate that an input value is a non-empty string.

    input_value: The input value to validate.
    field_name: The name of the input field (for error messages).
    return: None if input is valid, error message if not.
    """
    if not input_value or not isinstance(input_value, str) or not input_value.strip():
        return f"Invalid or missing {field_name}"
    return None

# Centralized error handler
def handle_error(error_type):
    """ 
    Return a JSON response for a given error type.
    Types are: invalid_input, file_not_found, internal_error, and not_found_in_corpus
    """
    error_info = ERROR_MESSAGES.get(error_type, ERROR_MESSAGES['internal_error'])
    return jsonify({"error": error_info['message']}), error_info['status_code']

# Flask routes

# Route for a friendly greeting
@app.route('/')
def hello():
    """
    Return a friendly HTTP greeting and list of available endpoints.
    """
    return """
    <h1>Welcome to the Search Engine API</h1>
    <p>This API provides the following endpoints:</p>
    <ul>
        <li><a href="/similar_words?w=word">/similar-words?w=word</a> - Find similar words</li>
        <li><a href="/find_similar_sentences?similar_words=word1,word2,word3">/find_similar_sentences?similar_words=word1,word2,word3</a> - Find similar sentences</li>
        <li><a href="/find_matching_sentences?input=word">/find_matching_sentences?input=word</a> - Find sentences containing a word</li>
        <li><a href="/add_word" target="_blank">/add_word</a> - Add a new word to the search corpus</li>
        <li><a href="/remove_similar_word?word=target_word">/remove_similar_word?word=target_word</a> - Remove the most similar word to a target word</li>
        <li><a href="/replace_word" target="_blank">/replace_word</a> - Replace all occurrences of a word in the search corpus</li>
        <li><a href="/get_corpus">/get_corpus</a> - Get the current search corpus</li>
    </ul>
    """

# Route to find similar words
@app.route('/similar_words', methods=['GET'])
def get_similar_words():
    """Find similar words to a query word."""
    try:
        query_word = request.args.get('w')

        # Validate the input query word
        error = validate_input_string(query_word, 'query_word')
        if error:
            return handle_error('invalid_input')

        # Use your custom similarity calculation logic with the custom vocabulary
        similar_words = find_most_similar_words(query_word, custom_vocab, word_list)

        # Return the results as JSON
        return jsonify({"query_word": query_word, "similar_words": similar_words})
    except Exception as exc: # pylint: disable=W0718
        logging.warning("Error processing request: %s", exc)
        return handle_error('internal_error')

# route to find similar sentences
@app.route('/find_similar_sentences', methods=['GET'])
def find_similar_sentences():
    """ This function finds similar sentences for a list of similar words"""
    try:
        # Get up to 3 similar words from '/similar-words'
        similar_words = request.args.get('similar_words')
        similar_words = similar_words.split(',')[:3]

        # Initialize a list to store matching sentences for similar words
        matching_sentences = []

        # Loop through each similar word and find matching sentences
        for word in similar_words:
            matching_sentences.extend(find_matching_sentences_for_word(word))

        return jsonify({"matching_sentences": matching_sentences})

    except Exception as exc: # pylint: disable=W0718
        logging.warning("Error processing request: %s", exc)
        return handle_error('internal_error')

# Define the route to find matching sentences for a single word
@app.route('/find_matching_sentences', methods=['GET'])
def find_matching_sentences():
    """
    Find sentences containing a word.

    Expects 'input' as a query parameter specifying the word to search for.
    """
    input_word = request.args.get('input')

    try:
        matching_sentences = find_matching_sentences_for_word(input_word)
        return jsonify({"matching_sentences": matching_sentences})

    except Exception as exc: # pylint: disable=W0718
        logging.warning("Error processing request: %s", exc)
        return handle_error('internal_error')


# Route to add a new word to the corpus
@app.route('/add_word', methods=['POST'])
def add_word():
    """
    Add a new word to the corpus.

    Expects a JSON object with a 'word' field specifying the new word.
    """
    try:
        data = request.get_json()
        new_word = data.get('word')

        if new_word is None:
            return handle_error('invalid_input')  # Use handle_error for missing 'word' parameter

        # Validate new_word using the input validation function
        validation_error = validate_input_string(new_word, 'new word')
        if validation_error:
            return handle_error('invalid_input')  # Use handle_error for validation error

        word_list.append(new_word)
        saved_word_list = save_corpus(CORPUS_FILE_PATH, word_list)

        if saved_word_list is None:
            logging.error("Failed to save the updated corpus.")
            return handle_error('internal_error')  # Use handle_error for internal error

        return jsonify({"message": f"Word '{new_word}' added to the corpus"}), 201

    except IOError as exc:
        logging.error("IO error while adding a word: %s", exc)
        return handle_error('internal_error')  # Use handle_error for internal error
    except Exception as exc:  # pylint: disable=W0718
        logging.error(
            "An unexpected error occurred while adding a word: %s", exc)
        return handle_error('internal_error')  # Use handle_error for internal error


@app.route('/remove_similar_word', methods=['DELETE'])
def remove_similar_word():
    """
    Remove the most similar word to a target word.

    Expects 'word' as a query parameter specifying the target word to remove.
    """
    try:
        target_word = request.args.get('word')

        # Validate target_word using the input validation function
        validation_error = validate_input_string(target_word, 'target word')
        if validation_error:
            return handle_error('invalid_input')  # Use handle_error for validation error

        removed_count = 0

        # Remove all occurrences of the target word from the corpus
        while target_word in word_list:
            word_list.remove(target_word)
            removed_count += 1

        if removed_count > 0:
            saved_word_list = save_corpus(CORPUS_FILE_PATH, word_list)

            if saved_word_list is None:
                logging.error(
                    "Failed to save the updated corpus while removing a similar word.")
                return handle_error('internal_error')

            message = f"Removed {removed_count} occurrences of word '{target_word}' from the corpus"
            return jsonify({"message": message}), 200

        error_message = f"No occurrences of word '{target_word}' found in the corpus"
        return jsonify({"error": error_message}), 404

    except KeyError as exc:
        error_message = f"Key error: {exc}"
        logging.error("Key error while removing a similar word: %s", exc)
        return handle_error('internal_error')
    except Exception as exc: # pylint: disable=W0718
        error_message = f"An unexpected error occurred: {exc}"
        logging.error(
            "An unexpected error occurred while removing a similar word: %s", exc)
        return handle_error('internal_error')


@app.route('/replace_word', methods=['PUT'])
def replace_word():
    """
    Replace all occurrences of a word in the corpus.

    Expects a JSON object with 'old_word' and 'new_word' fields to specify the replacement.
    """
    try:
        data = request.get_json()
        old_word = data.get('old_word')
        new_word = data.get('new_word')

        # Validate old_word and new_word using the input validation function
        validation_error_old = validate_input_string(old_word, 'old word')
        validation_error_new = validate_input_string(new_word, 'new word')

        if validation_error_old:
            return handle_error('invalid_input')  # Use handle_error for validation error

        if validation_error_new:
            return handle_error('invalid_input')  # Use handle_error for validation error

        replaced_count = 0

        # Replace all occurrences of old_word with new_word in the corpus
        for index, word in enumerate(word_list):
            if word.lower() == old_word.lower():
                word_list[index] = new_word
                replaced_count += 1

        save_corpus(CORPUS_FILE_PATH, word_list)

        if replaced_count > 0:
            return jsonify({"message": f"Replaced {replaced_count} \
                            occurrences of '{old_word}' with '{new_word}' in the corpus"}), 200

        return handle_error('not_found_in_corpus')  # Use handle_error for not found in the corpus

    except Exception as exc: # pylint: disable=W0718
        logging.error(
            "An unexpected error occurred while replacing a word: %s", exc)
        return handle_error('internal_error')


@app.route('/get_corpus', methods=['GET'])
def get_corpus():
    """
    Get the current corpus as a JSON response.
    """
    try:
        return jsonify({"corpus": word_list})
    except Exception as exc: # pylint: disable=W0718
        logging.error(
            "An unexpected error occurred while retrieving the corpus: %s", exc)
        return handle_error('internal_error')  # Use handle_error for internal error

# Start the Flask app if the script is executed directly
if __name__ == '__main__':
    app.run(debug=True)
