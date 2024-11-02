import subprocess
import argparse

# Define functions to run each script
def run_standardize_input():
    print("Running standardize_input.py...")
    subprocess.run(["python3", "./test_erroneous_data/standardize_input.py"])
 
def run_create_datasets():
    print("Running create_datasets.py...")
    subprocess.run(["python3", "./test_erroneous_data/create_datasets.py"])

def run_benchmark_script():
    print("Running benchmark_script.py...")
    subprocess.run(["python3", "benchmark_script.py"])

def run_visualize_benchmark():
    print("Running visualize_benchmark_data.py...")
    subprocess.run(["python3", "visualize_benchmark_data.py"])

def run_all():
    print("Running all scripts in order...")
    run_standardize_input()
    run_create_datasets()
    run_benchmark_script()
    run_visualize_benchmark()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run individual scripts or the entire workflow"
    )
    parser.add_argument(
        "script",
        type=str,
        nargs="?",
        choices=["standardize", "create", "benchmark", "visualize", "all"],
        help="Specify which script to run, or choose 'all' to run all scripts sequentially.",
    )

    args = parser.parse_args()

    # Map argument to function
    if args.script == "standardize":
        run_standardize_input()
    elif args.script == "create":
        run_create_datasets()
    elif args.script == "benchmark":
        run_benchmark_script()
    elif args.script == "visualize":
        run_visualize_benchmark()
    elif args.script == "all":
        run_all()
    else:
        print("Please specify a script to run (standardize, create, benchmark, visualize) or use 'all' to run the entire workflow.")
