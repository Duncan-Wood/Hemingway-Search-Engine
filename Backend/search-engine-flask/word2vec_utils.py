# word2vec_utils.py
"""Utility functions for the Word2Vec model."""
import logging
import numpy as np

# Cosine similarity is used with the Word2Vec PKL file to find similar words
def cosine_similarity(vec1, vec2):
    """Calculate the cosine similarity between two vectors."""
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)

    if norm_vec1 == 0 or norm_vec2 == 0:
        return 0  # Handle division by zero

    return dot_product / (norm_vec1 * norm_vec2)


def find_most_similar_words(
        query_word, custom_vocab, word_list, num_results=3, similarity_threshold=0):
    """Find the most similar words to a query word in a given list of words."""
    try:
        # Find similar words with a lower similarity threshold
        similar_words = []

        # Get the vector for the query word from the custom vocabulary
        if query_word in custom_vocab:
            query_vector = custom_vocab[query_word]
        else:
            raise KeyError("Query word not found in custom vocabulary")

        # Calculate similarity scores for each word in the word_list
        for word in word_list:
            if word != query_word and word in custom_vocab:
                word_vector = custom_vocab[word]
                similarity_score = cosine_similarity(query_vector, word_vector)

                if similarity_score >= similarity_threshold:
                    similar_words.append((word, similarity_score))

        # Sort the similar words by similarity score in descending order
        similar_words.sort(key=lambda x: x[1], reverse=True)

        # Extract the top num_results words
        similar_words = similar_words[:num_results]

        # Return the top num_results words
        return {"query_word": query_word, "similar_words": [word for word, _ in similar_words]}
    except KeyError as exc:
        logging.error("Key error while finding similar words: %s", exc)
        raise KeyError("Word not found in custom vocabulary") from exc
    