import pandas as pd
from pathlib import Path
import extraction as ex
import cleaning as cl
import transforming as tr
import db_load as ld
import cancelled_extract as ce

project_root = Path(__file__).resolve().parent.parent
raw_data_dir = project_root / "data" / "raw"
csv_files = list(raw_data_dir.glob("*.csv"))

all_datasets = ex.extract(csv_files)
merged_df = tr.transform(all_datasets)
cancelled_trips_df = ce.extract_cancelled_trips(merged_df)
cleaned_df = cl.clean_data(merged_df)

merged_df.to_csv(f"{project_root}/data/merged/combined_dataset.csv", index=False)
cleaned_df.to_csv(f"{project_root}/data/merged/combined_cleaned_dataset.csv", index=False)
cancelled_trips_df.to_csv(f"{project_root}/data/merged/combined_cancelled_trips_dataset.csv", index=False)

#ld.load(merged_df)

cleaned_df.info()