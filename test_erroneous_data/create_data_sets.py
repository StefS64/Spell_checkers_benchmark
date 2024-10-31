import json
import os
# TODO Create a user interaction system (maybe don't create all of data sets but only some).
# TODO Right now just create a working benchmark for one directory.
# TODO If multiple sources of data will be used standarize tha data.



# Specify the directory containing your JSON files
directory_path = './test_erroneous_data/standardized_input/single_words' 

# Dictionary to store all loaded JSON data, keyed by filename
correct_word_dictionaries = {}

# Get valid filenames
valid_filenames = []
for filename in os.listdir(directory_path):
    if filename.endswith('.json'):
        valid_filenames.append(filename)


# Loop through each file in the directory
for filename in valid_filenames:
    file_path = os.path.join(directory_path, filename)
    with open(file_path, 'r') as file:
        data = json.load(file)
        correct_word_dictionaries[filename] = data

# Now 'correct_word_dictionaries' contains all JSON contents, accessible by filename
print(correct_word_dictionaries)

for filename in valid_filenames:
    