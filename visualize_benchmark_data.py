import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

file_path = './benchmarks/benchmarks'


with open(file_path, 'r') as file:
    data = json.load(file)
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
        accuracies.append(metrics["Accuracy"] * 100)

# Create DataFrame
df = pd.DataFrame({
    "Checker": checker_names,
    "Dataset": datasets,
    "Correct": correct_counts,
    "Queries": query_counts,
    "Accuracy": accuracies
})


# Display the DataFrame
# print("Data for Visualization:\n", df)


# # Visualization using seaborn for clarity and style
# sns.set(style="whitegrid")
# plt.figure(figsize=(12, 6))

# # Create a bar plot for Accuracy across datasets for each spell checker
# sns.barplot(x="Dataset", y="Accuracy", hue="Checker", data=df)

# # Add title and labels
# plt.title("Accuracy of Spell Checkers across Datasets")
# plt.xlabel("Dataset")
# plt.ylabel("Accuracy")
# plt.ylim(0, 1.1)  

# plt.legend(title="Spell Checker")
# plt.tight_layout()
# plt.show()
sns.set_theme(style="whitegrid")
plt.figure(figsize=(12, 6))
bar_plot = sns.barplot(x="Dataset", y="Accuracy", hue="Checker", data=df)

# Customize the x-axis labels to include number of queries
dataset_labels = []
for dataset in df['Dataset'].unique():
    num_queries = df[df['Dataset'] == dataset]['Queries'].iloc[0]
    dataset_labels.append(f"{dataset}\n(Queries: {num_queries})")

# Apply custom labels
bar_plot.set_xticklabels(dataset_labels)
plt.gca().set_yticklabels([f"{int(y)}%" for y in bar_plot.get_yticks()])

# Add title and labels
plt.title("Accuracy of Spell Checkers across Datasets")
plt.xlabel("Dataset")
plt.ylabel("Accuracy")
plt.ylim(0, 100)
plt.legend(title="Spell Checker")
plt.tight_layout()
plt.show()