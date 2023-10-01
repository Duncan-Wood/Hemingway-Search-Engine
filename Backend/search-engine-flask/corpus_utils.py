""" Helper functions for corpus operations. """
import logging
import re
# will continue to develop this to include more file operations 
# that are currently in other files

# Helper function for file operations
def file_operation(file_path, operation, data=None, encoding='utf-8'):
    """
    Helper function for file operations.

    :param file_path: The path to the file.
    :param operation: The operation to perform ('read' or 'write').
    :param data: Data to write to the file (only used for 'write' operation).
    :param encoding: The encoding for file operations.
    :return: Success message or error message.
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

    :param file_path: The path to the corpus file.
    :return: List of words from the corpus.
    """
    try:
        corpus_text = file_operation(file_path, 'read')
        # Use regular expression to split corpus_text into words
        # This pattern splits text by spaces or punctuation, while preserving words with punctuation
        words = re.findall(r'\b\w+\b|[\.,!?;]', corpus_text)
        return words
    except FileNotFoundError as exc:
        raise exc
