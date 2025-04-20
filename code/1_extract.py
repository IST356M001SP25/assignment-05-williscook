import pandas as pd
import numpy as np
import streamlit as st
import pandaslib as pl
  
#TODO Write your extraction code here

# step 1: Read Survery Responses from a Google sheet as CSV

# Read the CSV file directly fom a shared Google Sheet Link
survey = pd.read_csv('https://docs.google.com/spreadsheets/d/1IPS5dBSGtwYVbjsfbaMCYIWnOuRmJcbequohNxCyGVw/export?resourcekey=&gid=1625408792&format=csv')

# Step 2: Extract Year from the Timestamp Column

# Apply a custom function to extract the year from dates in 'Timestamp' (assuming format is MM/DD/YYYY)
survey['year'] = survey['Timestamp'].apply(pl.extract_year_mdy)

# Step 3: Save survey data locally for caching

# Save the cleaned and processed survey data to a CSV file in the 'Cache' folder
survey.to_csv('cache/survey.csv', index=False)

# Step 4: Get all unique years from the survey data

# Get a list of all unique years found in the survey responses
years = survey['year'].unique()


# Step 5: For each year, download cost of living data

# Loop through each unique year found in the survey
for year in years:
    # Download the cost of living ranking table for that year from Numbeo (it return a list of tables)
    col_year = pd.read_html(f"https://www.numbeo.com/cost-of-living/rankings.jsp?title={year}&displayColumn=0")

    # Select the second table in the list (index=1) - this is assumed to be the correct table
    col_year = col_year[1]

    # Add a new column called 'year' to the table to keep track of the source year
    col_year['year'] = year

    # Save the processed cost of living data for the year into a seperate CSV in the cache folder
    col_year.to_csv(f'cache/col_{year}.csv', index=False)

# Step 6: Read state mapping table from another Google Sheet

# URL of a second Google Sheet that contains state-related data (e.g., name, region, abbreviation)
url = "https://docs.google.com/spreadsheets/d/14wvnQygIX1eCVo7H5B7a96W1v5VCg6Q9yeRoESF6epw/export?format=csv"

# Read the state table into a DataFrame
state_table = pd.read_csv(url)

# Save the state mapping table to a local CSV file for caching purposes
state_table.to_csv('cache/states.csv', index=False)   


