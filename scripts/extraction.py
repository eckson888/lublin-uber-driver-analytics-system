import pandas as pd

def extract(filepaths):
    datasets = [pd.read_csv(fp) for fp in filepaths]
    return datasets
