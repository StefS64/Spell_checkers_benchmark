import json
import os
import random
import pandas as pd
from tqdm import tqdm
# TODO Create a user interaction system (maybe don't create all of data sets but only some).
# TODO Right now just create a working benchmark for one directory.
# TODO add skew types think of a smart way
BATCH_SIZE = 1000
NUMBER_OF_WORD_VARIATIONS = 10


# Specify the directory containing your JSON files
source_directory_path = './test_erroneous_data/standardized_data/single_words' 
destination_directory_path = './test_erroneous_data/test_words' 
# Dictionary to store all loaded JSON data, keyed by filename
correct_word_dictionaries = {}

# Get valid filenames
valid_filenames = []
for filename in os.listdir(source_directory_path):
    if filename.endswith('.json'):
        valid_filenames.append(filename)


# Loop through each file in the directory
for filename in valid_filenames:
    file_path = os.path.join(source_directory_path, filename)
    with open(file_path, 'r') as file:
        data = json.load(file)
        correct_word_dictionaries[filename] = data

# Now 'correct_word_dictionaries' contains all JSON contents, accessible by filename

def subtract_letter(word):
    if len(word) > 1:
        position = random.randint(0, len(word) - 1)
        return word[:position] + word[position + 1:]
    
def replace_letter(word):
    position = random.randint(0, len(word) - 1)
    return word[:position] + chr(random.randint(32, 126)) + word[position + 1:]

def add_letter(word):
    position = random.randint(0, len(word) - 1)
    return word[:position] + chr(random.randint(32, 126)) + word[position:]

def create_augmented_word(word):
    transformations = [
        lambda w: subtract_letter(w),
        lambda w: w,
        lambda w: replace_letter(w),
        lambda w: add_letter(w)
    ]
    
    transformation = random.choice(transformations)
    incorrect_word = transformation(word)
    
    return incorrect_word


def process_in_batches(dictionary, write_file, batch_size=BATCH_SIZE, variation=NUMBER_OF_WORD_VARIATIONS):
    data_frame = pd.DataFrame({"Input": [],"Correct": []})
    keys = list(dictionary.keys())
    for i in tqdm(range(0, len(keys), batch_size)):
        new_data = []
        batch_words = keys[i:i + batch_size]  # Get the current batch of keys
        # print(f"Processing batch {i // batch_size + 1} (Keys: {batch_words})")
        for word in batch_words:
            for i in range(variation):
                generated_word = create_augmented_word(word)
                # We check if the generated word is perhaps a valid word.
                # If thats the case we abort creating the test.
                if generated_word != word and generated_word not in dictionary: 
                    new_data.append({"Input": generated_word, "Correct": word})  # Print the incorrect to correct mapping
        new_df = pd.DataFrame(new_data)
        data_frame = pd.concat([data_frame, new_df], ignore_index=True)
    data_frame.to_json(write_file, orient="records", lines=True)

for filename in valid_filenames:
    words = correct_word_dictionaries[filename]
    print(f"Creating test batch from {filename}")
    process_in_batches(words, os.path.join(destination_directory_path, filename))
