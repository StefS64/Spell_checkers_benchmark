import json
import os

# Specify the directory containing your JSON files
directory_path = './test_erroneous_data/raw_data/single_words' 

# Dictionary to store all loaded JSON data, keyed by filename
correct_word_dictionaries = {}

# Loop through each file in the directory
for filename in os.listdir(directory_path):
    if filename.endswith('.json'): 
        file_path = os.path.join(directory_path, filename)
        with open(file_path, 'r') as file:
            data = json.load(file)
            correct_word_dictionaries[filename] = data

# Now 'correct_word_dictionaries' contains all JSON contents, accessible by filename
print(correct_word_dictionaries[:5])

