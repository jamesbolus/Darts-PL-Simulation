# Import relevant packages
import matplotlib.pyplot as plt
import os
import bz2
import tarfile
import json
from datetime import datetime
import pandas as pd
import numpy as np
import re

# Step 1: Read and slightly alter dataframe including each PL match
results_df = pd.read_excel("../../../Darts SR/results.xlsx", index_col=False)

# Convert from "Surname, Forename" to "Forname Surname" (Betfair's entries are in this format)
results_df["home_bf"] = results_df["home"].apply(lambda x: f"{x.split(', ')[1]} {x.split(', ')[0]}")
results_df["away_bf"] = results_df["away"].apply(lambda x: f"{x.split(', ')[1]} {x.split(', ')[0]}")

# Step 2: Extract from .tar format (provided by Betfair) to .JSON format

# My .tar files were names "mm_dd.tar". Loop through each date and make a list of all .tar filenames needed.
tar_paths = []
for date in results_df["date"].drop_duplicates():
    month_string = datetime.strptime(date, '%Y-%m-%d').date().strftime('%m')
    day_string = datetime.strptime(date, '%Y-%m-%d').date().strftime('%d')
    string = f"{month_string}_{day_string}.tar"
    tar_paths.append(string)

# Loop through reading each tar file. This extracts them to be a .bz2 file
for tar_path in tar_paths:
    with tarfile.open(tar_path, 'r') as tar:
        # Extract all files to directory
        tar.extractall()


# Unzip bz2 files to JSON
root_dir = 'BASIC'

for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename.endswith('.bz2'):
            bz2_file_path = os.path.join(dirpath, filename)
            output_file_name = os.path.splitext(filename)[0] + '.json'
            output_file_path = os.path.join(dirpath, output_file_name)

            try:
                # Extract the .bz2 file
                with bz2.open(bz2_file_path, 'rt', encoding='utf-8') as bz2_file:
                    content = bz2_file.read()
                with open(output_file_path, 'w', encoding='utf-8') as output_file:
                    output_file.write(content)

                print(f"Extracted: {bz2_file_path} to {output_file_path}")

                # Delete the read .bz2 file
                os.remove(bz2_file_path)
                print(f"Deleted: {bz2_file_path}")

            except Exception as e:
                print(f"Failed to extract {bz2_file_path}: {e}")
