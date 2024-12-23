import pandas as pd
import os
import glob

# Define the file paths
mdrm_path = 'C:/Users/angel/Documents/Economics/Research/Banking Project/data/raw/MDRM'
cr_path = 'C:/Users/angel/Documents/Economics/Research/Banking Project/data/raw/CallReports_SinglePeriod/_extracted/'

# Define the path to save the data:
path_save = 'C:/Users/angel/Documents/Economics/Research/Banking Project/data/intermediate/call_reports_SP/'

# Path with FED computer 
#cr_path = 'C:/Users/IRAXA11/Documents/Research/Banking Project/Call Reports'
#mdrm_path = 'C:/Users/IRAXA11/Documents/Research/Banking Project/MDRM'


# Read MDRM_CSV.csv with a tab separator:
mdrm = pd.read_csv(mdrm_path + '/MDRM_CSV.csv', header=1, sep=',', low_memory=False)
mdrm['var_name'] = mdrm['Mnemonic'] + mdrm['Item Code']

# Get unique variable names in MDRM data
mdrm_names = mdrm.groupby(['var_name', 'Item Name']).size().reset_index().drop(columns=0)


def ingest(cr_path):

    # Set path to be the directory:
    os.chdir(cr_path)

    # Create a list with the last 8 digits of the names of the folders:
    dates = [folder[-8:] for folder in os.listdir()]  

    for date in dates:

        # Change the directory to the folder with the data:
        os.chdir(cr_path + 'FFIEC CDR Call Bulk All Schedules ' + date)
        
        # Load the data
        rc = pd.read_csv('FFIEC CDR Call Schedule RC '+date+'.txt', sep='\t').drop(index=0).reset_index(drop=True)
        rca = pd.read_csv('FFIEC CDR Call Schedule RCA '+date+'.txt', sep='\t').drop(index=0).reset_index(drop=True)
        rce1 = pd.read_csv('FFIEC CDR Call Schedule RCEI '+date+'.txt', sep='\t').drop(index=0).reset_index(drop=True)
        por = pd.read_csv('FFIEC CDR Call Bulk POR '+date+'.txt', sep='\t').drop(index=0).reset_index(drop=True)
        rck = pd.read_csv('FFIEC CDR Call Schedule RCK '+date+'.txt', sep='\t').drop(index=0).reset_index(drop=True)
        ri = pd.read_csv('FFIEC CDR Call Schedule RI '+date+'.txt', sep='\t').drop(index=0).reset_index(drop=True)
        
        # Define 'rcl' based on file availability
        rco_files = glob.glob(f'FFIEC CDR Call Schedule RCO {date}*.txt')
        
        if len(rco_files) == 1:
            rco = pd.read_csv(rco_files[0], sep='\t').drop(index=0).reset_index(drop=True)
        elif len(rco_files) == 2:
            rco = pd.read_csv(rco_files[0], sep='\t').drop(index=0).reset_index(drop=True)  # Only load '(1 of 2).txt'

        # Define 'rcl' based on file availability
        rcb_files = glob.glob(f'FFIEC CDR Call Schedule RCB {date}*.txt')
        
        if len(rcb_files) == 1:
            rcb = pd.read_csv(rcb_files[0], sep='\t').drop(index=0).reset_index(drop=True)
        elif len(rcb_files) == 2:
            rcb = pd.read_csv(rcb_files[0], sep='\t').drop(index=0).reset_index(drop=True)  # Only load '(1 of 2).txt'

        # drop 'RCON1773' column if it exists:
        if 'RCON1773' in rcb.columns:
            rcb = rcb.drop(columns='RCON1773')

        # Merge the data on 'IDRSSD':
        dt = pd.merge(rc, rca, on='IDRSSD')
        dt = pd.merge(dt, rce1, on='IDRSSD')
        dt = pd.merge(dt, por, on='IDRSSD')
        dt = pd.merge(dt, rck, on='IDRSSD')
        dt = pd.merge(dt, ri, on='IDRSSD')
        dt = pd.merge(dt, rco, on='IDRSSD')
        dt = pd.merge(dt, rcb, on='IDRSSD')
        #dt = pd.merge(dt, rcl, on='IDRSSD')
        #dt = dt.iloc[:, :-1]            # Drop last column since it is always empty
        dt['Date'] = date

        
        
        # Save 'long' data to a csv file in the folder data/intermediate/call_reports:
        dt.to_csv(path_save + date[-8:] + '.csv', index=False)
        #long.to_csv('C:/Users/IRAXA11/Documents/Research/Banking Project/Call Reports/' + f_path[-16:-4] + '.csv', index=False)


ingest(cr_path)
