import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

file_path = './benchmarks/benchmarks'


with open(file_path, 'r') as file:
    data = json.load(file)
print(data)
checker_names = []
datasets = []
correct_counts = []
query_counts = []
accuracies = []

for checker, checker_data in data.items():
    for dataset, metrics in checker_data.items():
        checker_names.append(checker)
        datasets.append(dataset)
        correct_counts.append(metrics["Correct:"])
        query_counts.append(metrics["Number_of_queries:"])
        accuracies.append(metrics["Accuracy"])

# Create DataFrame
df = pd.DataFrame({
    "Checker": checker_names,
    "Dataset": datasets,
    "Correct": correct_counts,
    "Queries": query_counts,
    "Accuracy": accuracies
})

# Display the DataFrame
print("Data for Visualization:\n", df)