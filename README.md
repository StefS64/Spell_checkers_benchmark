# Spellcheckers benchmarks.

## The data is already generated and benchmarks are visible


## Reproduction of results:
### Setup:

    - use 'script_name' script to install the right checkers onto your computer.
    pip install pyspellchecker textblob language-tool-python
    pip install datasets
### Visualize results:
    python3 -m controller.py visualize
### Run a new Benchmark:
    For different data size change config.py in test_erroneous_data/
    For different benchmark batch size change Benchmark size in benchmark_script.py
    '''
    python3 -m controller.py all
    '''




