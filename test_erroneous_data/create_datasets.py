import json
import os
import string
import random
import pandas as pd
from tqdm import tqdm
# TODO Create a user interaction system (maybe don't create all of data sets but only some).
# TODO add skew types think of a smart way
import config  # Importing the configuration file

BATCH_SIZE = config.BATCH_SIZE
NUMBER_OF_WORD_VARIATIONS = config.NUMBER_OF_WORD_VARIATIONS
DATA_SIZE_WORDS = config.DATA_SIZE_WORDS
DATA_SIZE_SENTENCES = config.DATA_SIZE_SENTENCES
LETTERS = config.LETTERS

source_directory_path_words = config.SOURCE_DIRECTORY_PATH_WORDS
source_directory_path_sentences = config.SOURCE_DIRECTORY_PATH_SENTENCES
destination_directory_path_words = config.DESTINATION_DIRECTORY_PATH_WORDS
destination_directory_path_sentences = config.DESTINATION_DIRECTORY_PATH_SENTENCES 

# Dictionary to store all loaded JSON data, keyed by filename
correct_word_dictionaries = {}

# Get valid filenames
# Now 'correct_word_dictionaries' contains all JSON contents, accessible by filename

def subtract_letter(word):
    if len(word) > 1:
        position = random.randint(0, len(word) - 1)
        return word[:position] + word[position + 1:]
    else:
        return word
    
def replace_letter(word):
    position = random.randint(0, len(word) - 1)
    return word[:position] + random.choice(LETTERS) + word[position + 1:]

def add_letter(word):
    position = random.randint(0, len(word) - 1)
    return word[:position] + random.choice(LETTERS) + word[position:]

def create_augmented_word(word):
    transformations = [
        lambda w: subtract_letter(w),
        lambda w: w,
        lambda w: replace_letter(w),
        lambda w: add_letter(w)
    ]
    
    transformation = random.choice(transformations)
    return transformation(word)

def change_words(sentence):
    words = sentence.split(' ')

    num_changes = random.randint(1,len(words))
    
    # Randomly select indices to change
    indices_to_change = random.sample(range(len(words)), num_changes)
    
    # Change the selected words
    for index in indices_to_change:
        words[index] = create_augmented_word(words[index]) 
    
    # Join the words back into a sentence
    return ' '.join(words)



def duplicate_word(sentence):
    words = sentence.split(' ')
    
    index_to_duplicate = random.randint(0, len(words) - 1)
    word_to_duplicate = words[index_to_duplicate]
    
    words.insert(index_to_duplicate + 1, word_to_duplicate)
    
    return ' '.join(words)

def create_augmented_sentence(sentence):
    transformations = [
        lambda s: subtract_letter(s),
        lambda s: s,
        lambda s: replace_letter(s),
        lambda s: add_letter(s),
        lambda s: change_words(s),
        lambda s: duplicate_word(s)
    ]
    transformation = random.choice(transformations)
    return transformation(sentence)

def create_augmented_key(key):
    if ' ' not in key:
        return create_augmented_word(key)
    else:
        return create_augmented_sentence(key)


def process_in_batches(dictionary, write_file, data_size, batch_size=BATCH_SIZE, variation=NUMBER_OF_WORD_VARIATIONS):
    data_frame = pd.DataFrame({"Input": [],"Correct": []})
    keys = list(dictionary.keys())
    for i in tqdm(range(0, data_size, batch_size)):
        new_data = []
        index = random.randint(0, len(keys))
        batch_keys = keys[index:index + min(batch_size, data_size - batch_size*i)]  # Get the current batch of keys
        # print(f"Processing batch {i // batch_size + 1} (Keys: {batch_words})")
        for key in batch_keys:
            for i in range(variation):
                generated_word = create_augmented_key(key)
                # We check if the generated word is perhaps a valid word.
                # If thats the case we abort creating the test.
                if generated_word != key and generated_word not in dictionary: 
                    new_data.append({"Input": generated_word, "Correct": key})
        new_df = pd.DataFrame(new_data)
        data_frame = pd.concat([data_frame, new_df], ignore_index=True)
    data_frame.to_json(write_file, orient="records", lines=True)


def create_data(source_path, destination_path, data_size):
    valid_filenames = []
    for filename in os.listdir(source_path):
        if filename.endswith('.json'):
            valid_filenames.append(filename)


    # Loop through each file in the directory
    for filename in valid_filenames:
        file_path = os.path.join(source_path, filename)
        with open(file_path, 'r') as file:
            data = json.load(file)
            correct_word_dictionaries[filename] = data

    for filename in valid_filenames:
        words = correct_word_dictionaries[filename]
        print(f"Creating test batch from \033[92m{filename}\033[0m")
        process_in_batches(words, os.path.join(destination_path, filename), data_size)

create_data(source_directory_path_words, destination_directory_path_words, DATA_SIZE_WORDS)
create_data(source_directory_path_sentences, destination_directory_path_sentences, DATA_SIZE_SENTENCES)