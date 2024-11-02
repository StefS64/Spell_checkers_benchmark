import pandas as pd
import os
import json
from tqdm import tqdm
from spell_checker_wrappers import *
import concurrent.futures

# Change this variable in need of batch increase
BATCH_SIZE = 80
spell_checkers = { 
    "PySpell": {"class": PySpellChecker(), "concurrent" : True},
    "TextBlob": {"class": TextBlobChecker(), "concurrent" : True},
    "OliverTransform": {"class": TransformersSpellChecker(), "concurrent" : False},
}
# "HunspellConcurrent": {"class": HunspellChecker(), "concurrent" : True}, "SymSpellConcurrent": {"class": SymSpellChecker(), "concurrent" : True}, "NorvigConcurrent": {"class": NorvigSpellChecker(), "concurrent" : True}}

# TODO add more datasets (not neccesarily local)
#
# using hugging face datasets
# from datasets import load_dataset

# dataset = load_dataset("pnr-svc/spellchecker-dataset")['train']
# print(dataset['correct'][:5])
# print(pyspell_checker.check(dataset['correct'][:5]))
# print(pyspell_checker.check("this text has problemsxx find hhem"))

# using created data sets
benchmark_directory_path = './benchmarks' 
datasets_directory_paths = ['./test_erroneous_data/test_words', './test_erroneous_data/test_sentences']
# TODO wrong_answers_path = './'
def compare_lists(list1, list2):
    if len(list1) != len(list2):
        return -1
    differ = 0
    for i in range(len(list1)):
        if list1[i] != list2[i]:
            differ += 1 
    return differ


def process_chunk(data_chunk, spell_checker):
    correct = 0
    input = data_chunk['Input'].to_list()
    output_list = spell_checker.check(input)
    correct += sum(a != b for a, b in zip(output_list, data_chunk['Correct'].to_list()))
    return correct

def benchmark_data(data, spell_checker, run_concurrent, batch_size=BATCH_SIZE):
    chunks = [data.iloc[i:i + batch_size] for i in range(0, len(data), batch_size)]
    correct = 0
    if run_concurrent:
        num_workers = os.cpu_count()
        with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
            results = list(tqdm(executor.map(process_chunk, chunks, [spell_checker]*len(chunks)), total=len(chunks)))
    else: 
        results = [process_chunk(chunk, spell_checker) for chunk in tqdm(chunks)]
    
    correct = sum(results)
    return {"Correct:": correct, "Number_of_queries:": len(data), "Accuracy": correct/len(data)}


def benchmark_on_all_local_datasets(spell_checker, checker_name):
    results = {}
    for datasets_path in datasets_directory_paths:
        for filename in os.listdir(datasets_path):
            if filename.endswith('.json'):
                file_path = os.path.join(datasets_path, filename)
                test_data = pd.read_json(file_path, lines=True)
                print(f"Benchmarking \033[92m{checker_name}\033[0m over data set: \033[92m{filename}\033[0m")
                results[filename] = benchmark_data(test_data, spell_checker['class'], spell_checker['concurrent'])
    return results


def create_benchmarks():
    benchmarks = {}
    for checker in spell_checkers.keys():
        benchmarks[checker] = benchmark_on_all_local_datasets(spell_checkers[checker], checker)
        print(benchmarks[checker])
    print(benchmarks)

    benchmarks_file = os.path.join(benchmark_directory_path,'benchmarks')
    with open(benchmarks_file, 'w') as json_file:
        json.dump(benchmarks, json_file)
create_benchmarks()

