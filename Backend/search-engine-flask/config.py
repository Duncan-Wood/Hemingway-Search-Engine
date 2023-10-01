# config.py
"""Configuration file for the Flask app."""

# Constants
CORPUS_FILE_PATH = "./corpus/hemingway.txt"
# Define the number of words to display before and after the search term
CONTEXT_SIZE = 30
# Define error constants
ERROR_MESSAGES = {
    'invalid_input': {'message': 'Invalid or missing input', 'status_code': 400},
    'file_not_found': {'message': 'Text file not found', 'status_code': 404},
    'value_error': {'message': 'Value error', 'status_code': 400},
    'internal_error': {'message': 'Internal server error', 'status_code': 500},
    'not_found_in_corpus': {'message': "No occurrences found in the corpus", 'status_code': 404},
}