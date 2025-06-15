import duckdb
import pandas as pd

# List of CSV files to load
csv_files = ['play_by_play_2024.csv', 'play_by_play_2023.csv', 'play_by_play_2022.csv', 
             'play_by_play_2021.csv', 'play_by_play_2020.csv', 'play_by_play_2019.csv',
             'play_by_play_2018.csv', 'play_by_play_2017.csv', 'play_by_play_2016.csv',
             'play_by_play_2015.csv', 'play_by_play_2014.csv', 'play_by_play_2013.csv',
             'play_by_play_2012.csv', 'play_by_play_2011.csv', 'play_by_play_2010.csv',
             'play_by_play_2009.csv', 'play_by_play_2008.csv', 'play_by_play_2007.csv',
             'play_by_play_2006.csv', 'play_by_play_2005.csv', 'play_by_play_2004.csv',
             'play_by_play_2003.csv', 'play_by_play_2002.csv', 'play_by_play_2001.csv',
             'play_by_play_2000.csv', 'play_by_play_1999.csv'
             ]

# Load the first file with header
df = pd.read_csv(csv_files[0])

# Load subsequent files, skipping the header row
for csv_file in csv_files[1:]:
    print(f"Loading {csv_file}...")
    temp_df = pd.read_csv(csv_file, header=0)
    df = pd.concat([df, temp_df], ignore_index=True)

# Connect to a DuckDB database file
con = duckdb.connect('nfl.duckdb')

# Save DataFrame to DuckDB
con.execute("DROP TABLE IF EXISTS play_by_play")
con.execute("CREATE TABLE play_by_play AS SELECT * FROM df")

con.close()