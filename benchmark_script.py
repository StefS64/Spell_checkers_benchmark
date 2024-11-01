import pandas as pd
import os
from tqdm import tqdm
from spell_checker_wrappers import *
BATCH_SIZE = 100
# TODO automate the spellcheckers for instance use a directory
spellCheckers = ["PySpellChecker", "test"]
pyspell_checker = PySpellChecker()


# using hugging face datasets
from datasets import load_dataset

dataset = load_dataset("pnr-svc/spellchecker-dataset")['train']
print(dataset['correct'][:5])
# print(pyspell_checker.check(dataset['correct'][:5]))
# print(pyspell_checker.check("this text has problemsxx find hhem"))


# using created data sets
benchmark_directory_path = './benchmarks' 
datasets_directory_path = './test_erroneous_data/test_words'
# TODO wrong_answers_path = './'
def compare_lists(list1, list2):
    if len(list1) != len(list2):
        return -1
    differ = 0
    for i in range(len(list1)):
        if list1[i] != list2[i]:
            differ += 1 
    return differ


def benchmark_batch(data, spell_checker, batch_size=BATCH_SIZE):
    correct = 0
    for i in tqdm(range(0, len(data), batch_size)):
        input = data['Input'][i:i+batch_size].to_list()    
        # print(input)
        output_list = spell_checker.check(input)
        correct += compare_lists(output_list, test_data['Correct'][i:i+batch_size].to_list())
    # return {"Correct:": correct, "Number_of_queries:": len(test_data), "Accuracy": correct/len(test_data)}
    return correct


spell_checker = spellCheckers[0]
for filename in os.listdir(datasets_directory_path):
    if filename.endswith('.json'):
        file_path = os.path.join(datasets_directory_path, filename)
        test_data = pd.read_json(file_path, lines=True)
        print(f"Benchmarking {spell_checker} over data set: {filename}")
        print(benchmark_batch(test_data))
