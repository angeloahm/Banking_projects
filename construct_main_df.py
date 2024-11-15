import pandas as pd 
import numpy as np
import os 

path = 'C:/Users/angel/Documents/Economics/Research/Banking Project/data/clean'

# Set path to be the directory:
os.chdir(path)

# Putting all date-files into one single .csv file
df = pd.concat([pd.read_csv(f) for f in os.listdir() if f.endswith('.csv')])

# check how many columns are in the data:
#n_col = df.shape[1]
#df = df.iloc[:, 0:n_col-2]

# Adjust date format
df['Date'] = df['Date'].astype(str)
df['Month'] = np.where(df['Date'].str.len() == 8, df['Date'].str[0:2], '0'+df['Date'].str[0])
df['Day'] = df['Date'].str[-6:-4]
df['Year'] = df['Date'].str[-4:]
df['Date'] = pd.to_datetime(df['Year'] + '-' + df['Month'] + '-' + df['Day'])

# Save main into a .csv file
df.to_csv('C:/Users/angel/Documents/Economics/Research/Banking Project/data/clean/call_reports.csv', index = False)