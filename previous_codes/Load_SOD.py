# Load packages:
import pandas as pd
import requests
import yaml

# Load the YAML file
yaml_file_path = 'c:\\Users\\angel\\Documents\\Economics\\Research\\Banking Project\\Banking_projects\\Dictionaries'
#yaml_file_path = 'C:\\Users\\IRAXA11\\Documents\\Research\\Banking Project\\FDIC Summary of Deposits\\Dictionaries'


# Read the 'sod_properties.yaml' file:
with open(yaml_file_path + '\\sod_properties.yaml', 'r') as file:
    sod_properties = yaml.safe_load(file)

# Take the keys of the dictionary:
keys = sod_properties['properties']['data']['properties'].keys()

# Join all properties into a single string
fields = ",".join(keys)


# Create the API to extract SOD data 
# Define the API endpoint and parameters
api_url = "https://banks.data.fdic.gov/api/sod"
params = {
    "fields": fields,           # Fields to retrieve
    "limit": 1000,               # Number of records to retrieve
    "offset": 0,                # Offset for pagination
    "sort_by": "CERT",          # Sort by CERT field
    "format": "json"            # Response format
}

# We may need more than one request to retrieve all the data. In this case we will use a loop to fetch all the records.
# We will store all the records in a list called all_records.

# Initialize an empty list to hold all records
all_records = []

# Fetch data with pagination
while True:
    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        data = response.json()
        records = [record['data'] for record in data['data']]
        all_records.extend(records)
        
        # Check if we have retrieved all the records
        if len(records) < params['limit']:
            break
        
        # Update the offset for the next request
        params['offset'] += params['limit']
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        break


# Convert to DataFrame
sod = pd.DataFrame(all_records)

# Save the data to a CSV file (not in the repository):
sod.to_csv('c:\\Users\\angel\\Documents\\Economics\\Research\\Banking Project\\data\\intermediate\\sod\\sod_data.csv', index=False)
#sod.to_csv('C:\\Users\\IRAXA11\\Documents\\Research\\Banking Project\\sod_data.csv', index=False)
