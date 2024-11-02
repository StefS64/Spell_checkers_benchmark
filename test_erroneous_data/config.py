# config.py
import string
# How big batches will the data be generated.
BATCH_SIZE = 500
# DATA_SIZE how many data will be pulled from the input files.
# Every pull from the data will create about 20 variations.
NUMBER_OF_WORD_VARIATIONS = 20
DATA_SIZE_WORDS = 1000
DATA_SIZE_SENTENCES = 800
LETTERS = string.ascii_letters

# Directory's containing specific files
SOURCE_DIRECTORY_PATH_WORDS = './test_erroneous_data/standardized_data/single_words'
SOURCE_DIRECTORY_PATH_SENTENCES = './test_erroneous_data/standardized_data/sentences'
DESTINATION_DIRECTORY_PATH_WORDS = './test_erroneous_data/test_words'
DESTINATION_DIRECTORY_PATH_SENTENCES = './test_erroneous_data/test_sentences'
