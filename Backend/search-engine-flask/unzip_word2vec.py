# This file is not used during the execution of the program.
# It is only used to unzip the GoogleNews word2vec file.
# I included it here for completeness.

""" Unzips the GoogleNews word2vec file. """
import gzip
import shutil

INPUT_FILE = '/Users/myname/Desktop/GoogleNews-vectors-negative300.bin.gz'
OUTPUT_FILE = '/Users/myname/Desktop/GoogleNews-vectors-negative300.bin'

with gzip.open(INPUT_FILE, 'rb') as f_in:
    with open(OUTPUT_FILE, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
