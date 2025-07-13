import requests
import pandas as pd
import os

CENSUS_API_KEY = os.getenv('CENSUS_API_KEY')
CENSUS_API_URL = 'https://api.census.gov/data/2023/acs/acs5'

CENSUS_API_PARAMS = {
    'get': 'NAME,B19013_001E', 
    'for': 'county:*',
    'in': 'state:24', 
    'key': CENSUS_API_KEY,
}

resp = requests.get(CENSUS_API_URL, params=CENSUS_API_PARAMS).json()

df = pd.DataFrame(resp[1:], columns=resp[0])
df.rename(columns={'B19013_001E': 'median_income'}, inplace=True)
df['median_income'] = pd.to_numeric(df['median_income'], errors='coerce')
df['county'] = df['NAME'].str.split(',').str[0]
df.drop(columns=['NAME'], inplace=True)
df['state'] = 'Maryland'
df = df[['state', 'county', 'median_income']]
df['median_income'] = df['median_income'].astype(float)

print(df.head())
