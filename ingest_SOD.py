# Load packages
import pandas as pd
import os


# Set path to SOD data:
sod_path = 'C:/Users/angel/Documents/Economics/Research/Banking Project/data/raw/Summary of Branch Deposits/Branches/_extracted'

# Get file paths for call reports
f_paths = [os.path.join(root, file) for root, _, files in os.walk(sod_path) for file in files if (file.endswith('_1.csv') or file.endswith('_2.csv'))]

# Loop over f_paths files to read them and concatenate them into a single DataFrame:
sod = pd.concat([pd.read_csv(f_path, header=0, sep=',', encoding='ISO-8859-1', 
                             low_memory=False) for f_path in f_paths])

# Write a .csv file with the concatenated data:
sod.to_csv('C:/Users/angel/Documents/Economics/Research/Banking Project/data/intermediate/sod/sod_data.csv', index=False)