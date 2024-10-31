import json
import shutil
import os
# This script converts raw_data to standardized_data.
# The standard data format will be a json file, 
# which has the following structure depending on the format of data:
# #       1. File contains correct words:
#             The data will be kept in a dictionary for time complexity sake.
#             My approach will use searching the data set.
#             The words will be keys to the same value 1.

#         2. TODO Valid Sentences



source_path_words = './test_erroneous_data/raw_data/single_words'
destination_path_words = './test_erroneous_data/standardized_data/single_words'

# word_dictionary_english has the right format.
# Thus we just create a copy.

def copy_to_destination(file_name):
    source_file = os.path.join(source_path_words, file_name)
    destination_file = os.path.join(destination_path_words, file_name)
    
    if not os.path.exists(destination_file):
        with open(destination_file, 'w') as json_file:
            json.dump({}, json_file)
        print(f"Created file: {destination_file}")
    else:
        print(f"File already exists: {destination_file}")

    try:
        shutil.copy(source_file, destination_file)
        print(f"Copied '{source_file}' to '{destination_file}'")
    except PermissionError:
        print(f"Permission denied for '{source_file}'.")
    except Exception as e:
        print(f"An error occurred while copying '{source_file}': {e}")



copy_to_destination('words_dictionary_english.json')