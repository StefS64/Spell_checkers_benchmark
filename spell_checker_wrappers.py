from spellchecker import SpellChecker
from transformers import pipeline

class PySpellChecker:
    def __init__(self):
        self.spell = SpellChecker()
    def check(self, text):
        if type(text) == str:
            words = text.split()
        else:
            words = text
        corrections = []
        for word in words:
            if word not in self.spell:
                correction = self.spell.correction(word)
                corrections.append((correction))
        return corrections

from textblob import TextBlob

class TextBlobChecker:
    def __init__(self):
        pass  # TextBlob does not require initialization parameters

    def check(self, text):
        # Check if the input is a list of words
        if isinstance(text, list):
            # Correct each word individually and return the list of corrected words
            corrected_words = [str(TextBlob(word).correct()) for word in text]
            return corrected_words
        else:
            # Convert the input text to a TextBlob object
            blob = TextBlob(text)
            # Correct the text using TextBlob's built-in method
            corrected_text = blob.correct()
            return str(corrected_text)

class TransformersSpellChecker:
    max_input_length = 1024
    def __init__(self):
        # Initialize the spelling correction pipeline
        self.spell_checker = pipeline("text2text-generation", model="oliverguhr/spelling-correction-english-base")

    def check(self, text):
        # If the input is a list, join it into a single string
        if isinstance(text, list):
            text = " ".join(text)   
        
        # If the string of words is to large create smaller chunks.
        corrected_output = []
        start = 0
        while start < len(text):
            end = min(start + self.max_input_length, len(text))# Transform can take in maximally 1024 characters into model.

            # Find the last space within the max_length range to avoid cutting off in the middle of a word
            if end < len(text) and text[end] != ' ':
                end = text.rfind(' ', start, end) 

            chunk = text[start:end]
            # Correct the current chunk
            corrected_chunk = self.spell_checker(chunk, max_length=self.max_input_length)[0]['generated_text']
            corrected_output.append(corrected_chunk)

            start = end + 1  # Move to the next chunk

        # Join all corrected chunks back together
        return " ".join(corrected_output)
        # Return the corrected text
        return corrected_output
