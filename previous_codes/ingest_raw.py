import pandas as pd
import os

# Define the file paths
#mdrm_path = 'C:/Users/angel/Documents/Economics/Research/Banking Project/data/raw/MDRM'
#cr_path = 'C:/Users/angel/Documents/Economics/Research/Banking Project/data/raw/Call Reports'

# Path with FED computer 
cr_path = 'C:/Users/IRAXA11/Documents/Research/Banking Project/Call Reports'
mdrm_path = 'C:/Users/IRAXA11/Documents/Research/Banking Project/MDRM'

# Read MDRM_CSV.csv with a tab separator:
mdrm = pd.read_csv(mdrm_path + '/MDRM_CSV.csv', header=1, sep=',', low_memory=False)
mdrm['var_name'] = mdrm['Mnemonic'] + mdrm['Item Code']

# Get unique variable names in MDRM data
mdrm_names = mdrm.groupby(['var_name', 'Item Name']).size().reset_index().drop(columns=0)

# Get file paths for call reports
f_paths = [os.path.join(root, file) for root, _, files in os.walk(cr_path) for file in files if file.endswith(').txt')]

def ingest(f_paths):
    for f_path in f_paths:
        # Read call report data
        dt = pd.read_csv(f_path, header=0, sep='\t')
        dt = dt.iloc[1:]
        var_names = dt.columns[13:-1]  # Drop last variable since it is always empty
        long = pd.melt(dt, id_vars=dt.columns[:13], value_vars=var_names, var_name='variable', value_name='value')
        long['value'] = pd.to_numeric(long['value'], errors='coerce')
        long['year'] = f_path[-16:-12]
        long = pd.merge(long, mdrm_names, left_on='variable', right_on='var_name', how='left')
        
        # Save 'long' data to a csv file in the folder data/intermediate/call_reports:
        long.to_csv('C:/Users/angel/Documents/Economics/Research/Banking Project/data/intermediate/call_reports/' + f_path[-16:-4] + '.csv', index=False)
        #long.to_csv('C:/Users/IRAXA11/Documents/Research/Banking Project/Call Reports/' + f_path[-16:-4] + '.csv', index=False)

    
ingest(f_paths)
