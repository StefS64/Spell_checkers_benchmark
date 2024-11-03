import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# File to show 
file_path = './benchmarks/benchmarks'

with open(file_path, 'r') as file:
    data = json.load(file)
checker_names = []
datasets = []
correct_counts = []
query_counts = []
accuracies = []
times = []


for checker, checker_data in data.items():
    for dataset, metrics in checker_data.items():
        checker_names.append(checker)
        datasets.append(dataset)
        correct_counts.append(metrics["Correct:"])
        query_counts.append(metrics["Number_of_queries:"])
        accuracies.append(metrics["Accuracy"] * 100)
        times.append(metrics["Time"])

df = pd.DataFrame({
    "Checker": checker_names,
    "Dataset": datasets,
    "Correct": correct_counts,
    "Queries": query_counts,
    "Accuracy": accuracies,
    "Time": times
})

sns.set_theme(style="whitegrid")
fig1 = plt.figure(figsize=(12, 6))
bar_plot = sns.barplot(x="Dataset", y="Accuracy", hue="Checker", data=df)

dataset_labels = []

for dataset in df['Dataset'].unique():
    num_queries = df[df['Dataset'] == dataset]['Queries'].iloc[0]
    dataset_labels.append(f"{dataset}\n(Queries: {num_queries})")

# Set y-axis labels to percentage
plt.gca().set_yticklabels([f"{int(y)}%" for y in bar_plot.get_yticks()])

fig, axes = plt.subplots(1, figsize=(12, 6))

sns.set_theme(style="whitegrid")
# Plot time taken
time_plot = sns.barplot(x="Dataset", y="Time", hue="Checker", data=df)
plt.gca().set_yticklabels([f"{y:.2f}s" for y in time_plot.get_yticks()])

for p in time_plot.patches:
    if p.get_height() > 0:
        print(p.get_height())
        time_plot.annotate(format(p.get_height(), '.1f'),
                        (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha = 'center', va = 'center',
                        xytext = (0, 9),
                        textcoords = 'offset points')

# set x-axis labels
bar_plot.set_xticklabels(dataset_labels)
time_plot.set_xticklabels(dataset_labels)

plt.tight_layout()  
fig1.savefig('./benchmarks/benchmark_accuracy_results.png')
fig.savefig('./benchmarks/benchmark_time_results.png')
plt.show()