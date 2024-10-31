from spellchecker import SpellChecker



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
                corrections.append((word, correction))
        return corrections