spellCheckers = ["PySpellChecker", "test"]

from spell_checker_wrappers import *

pyspell_checker = PySpellChecker()


# using hugging face datasets
from datasets import load_dataset

dataset = load_dataset("pnr-svc/spellchecker-dataset")['train']
print(dataset)
print(pyspell_checker.check(dataset['correct'][:5]))
print(pyspell_checker.check("this text has problemsxx find hhem"))





# 
