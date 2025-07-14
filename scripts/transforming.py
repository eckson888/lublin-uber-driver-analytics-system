import pandas as pd

def transform(datasets):
    all_columns = set().union(*(df.columns for df in datasets))

    datasets_with_id = []
    for idx, df in enumerate(datasets):
        df_copy = df.copy()
        df_copy['user_id'] = idx
        df_copy = df_copy.reindex(columns=all_columns.union(['user_id']))
        datasets_with_id.append(df_copy)

    dataset_combined = pd.concat(datasets_with_id, ignore_index=True)
    return dataset_combined
