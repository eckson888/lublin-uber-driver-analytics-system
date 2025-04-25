import pandas as pd
import cleaning as cl
def transform(datasets):
    all_columns = set().union(*(df.columns for df in datasets))
    datasets = [df.reindex(columns=all_columns) for df in datasets]
    dataset_combined = pd.concat(datasets, ignore_index=True)
    return dataset_combined