import pandas as pd 
import numpy as np
import os 

path = 'C:/Users/angel/Documents/Economics/Research/Banking Project/data/intermediate/call_reports_SP'

# Set path to be the directory:
os.chdir(path)

# Putting all date-files into one single .csv file
df = pd.concat([pd.read_csv(f) for f in os.listdir() if f.endswith('.csv')])

# check how many columns are in the data:
#n_col = df.shape[1]
#df = df.iloc[:, 0:n_col-2]

# make 'Date' a datetime object:
df['Date'] = pd.to_datetime(df['Date'], format='%m%d%Y')

# Save main into a .csv file
df.to_csv('C:/Users/angel/Documents/Economics/Research/Banking Project/data/clean/call_reports.csv', index = False)