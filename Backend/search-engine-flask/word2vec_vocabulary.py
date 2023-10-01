# this file is not used during the execution of the program.
# It is only used to create the vocabulary file.
# I did this because the vocabulary file is too large to upload to GitHub.
# I included it here for completeness.

# Version 3
""" This script creates a set of words found in the Word2Vec model and saves it to a file. """
import pickle
from gensim.models import KeyedVectors

# Load the pre-trained Word2Vec model outside the loop
word2vec_model = KeyedVectors.load_word2vec_format(
    '/Users/duncanwood/Desktop/GoogleNews-vectors-negative300.bin', binary=True)

# Create a set of all words in the Word2Vec model
word2vec_words = set(word2vec_model.index_to_key)

# Specify the file path where you want to save the vocabulary dictionary
VOCABULARY_FILE = 'vocabulary.pkl'

# Serialize and save the Word2Vec words to the file
with open(VOCABULARY_FILE, 'wb') as file:
    pickle.dump(word2vec_words, file)

# Version 2
# """ This script creates a set of words found in the Word2Vec model and saves it to a file. """
# import pickle
# from gensim.models import KeyedVectors
# import config # pylint: disable=E0401
# import corpus_utils # pylint: disable=E0401

# # Load the pre-trained Word2Vec model outside the loop
# word2vec_model = KeyedVectors.load_word2vec_format(
#     '/Users/duncanwood/Desktop/GoogleNews-vectors-negative300.bin', binary=True)

# # Create a set of all words in the Word2Vec model
# word2vec_words = set(word2vec_model.index_to_key)

# # Load your corpus words
# word_list = corpus_utils.load_corpus(config.CORPUS_FILE_PATH)

# # Create a dictionary of words and their vectors found in the Word2Vec model
# model_vocabulary_filtered = {}

# for word in word_list:
#     if word in word2vec_words:
#         model_vocabulary_filtered[word] = word2vec_model[word]

# # Specify the file path where you want to save the vocabulary dictionary
# VOCABULARY_FILE = 'vocabulary.pkl'

# # # Serialize and save the vocabulary dictionary to the file
# with open(VOCABULARY_FILE, 'wb') as file:
#     pickle.dump(model_vocabulary_filtered, file)

# Version 1
# """ This script creates a set of words found in the Word2Vec model and saves it to a file. """
# import pickle
# from gensim.models import KeyedVectors
# import config # pylint: disable=E0401
# import corpus_utils # pylint: disable=E0401

# word_list = corpus_utils.load_corpus(config.CORPUS_FILE_PATH)

# # Load the pre-trained Word2Vec model
# word2vec_model = KeyedVectors.load_word2vec_format(
#     '/Users/duncanwood/Desktop/GoogleNews-vectors-negative300.bin', binary=True)

# # Create a dictionary of words and their vectors found in the Word2Vec model
# model_vocabulary_filtered = {}

# for word in word_list:
#     if word in word2vec_model:
#         model_vocabulary_filtered[word] = word2vec_model[word]

# # Specify the file path where you want to save the vocabulary dictionary
# VOCABULARY_FILE = 'vocabulary.pkl'

# # Serialize and save the vocabulary dictionary to the file
# with open(VOCABULARY_FILE, 'wb') as file:
#     pickle.dump(model_vocabulary_filtered, file)
