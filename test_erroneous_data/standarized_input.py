import json
import shutil
import os
import nltk
from nltk.tokenize import sent_tokenize
nltk.download('punkt_tab')
import re
# This script converts raw_data to standardized_data.
# The standard data format will be a json file, 
# which has the following structure depending on the format of data:
# #       1. File contains correct words:
#             The data will be kept in a dictionary for time complexity sake.
#             My approach will use searching the data set.
#             The words will be keys to the same value 1.

#         2. File containing Valid sentences:
#                The data will be kept in a list.
#                Every list element is one row of the text


source_path_texts = './test_erroneous_data/raw_data/whole_texts'
source_path_words = './test_erroneous_data/raw_data/single_words'
destination_path_words = './test_erroneous_data/standardized_data/single_words'
destination_path_texts = './test_erroneous_data/standardized_data/sentences'
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

def parse_texts():
    replacements = {
        '\u2018': "'",  # Left single quotation mark
        '\u2019': "'",  # Right single quotation mark
        '\u201c': '"',  # Left double quotation mark
        '\u201d': '"',  # Right double quotation mark
        '\u2026': '...', # Ellipsis
        '\u2013': '-',   # En dash
        '\u2014': '-',   # Em dash
        '\n'    : " ",   # endl  
    }
    
    for file_name in os.listdir(source_path_texts):
        text_file = os.path.join(source_path_texts, file_name)
        
        with open (text_file, 'r', encoding='utf-8') as file: 
            text = file.read()
            for old, new in replacements.items():
                text = text.replace(old, new)
            text = re.sub(r'\s+', ' ', text).strip()
        sentences = sent_tokenize(text)
        destination_file = os.path.join(destination_path_texts, f"{os.path.splitext(file_name)[0]}.json")
        sentences_dict = {sentence: 1 for sentence in sentences}
        
        with open(destination_file, 'w') as json_file:
            json.dump(sentences_dict, json_file)
        print(f"Created file: {destination_file}")
    
copy_to_destination('words_dictionary_english.json')
parse_texts()