# Spellcheckers Benchmarks

## The data is already generated and benchmarks are visible.

## Reproduction of Results:

### Setup

Use `script_name` script to install the right checkers onto your computer.

    pip install pyspellchecker textblob language-tool-python
    pip install datasets

### Visualize Results

    python3 -m controller.py visualize

### Run a New Benchmark

- For different data sizes, change `config.py` in `test_erroneous_data/`.
- For different benchmark batch sizes, change `Benchmark size` in `benchmark_script.py`.

To run a full benchmark:

    python3 -m controller.py all
## Report
After visualizing the data we can se
