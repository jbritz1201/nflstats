import duckdb
import pandas as pd

# List of compressed CSV files to load
csv_files = [
    'play_by_play_2024.csv.gz', 'play_by_play_2023.csv.gz', 'play_by_play_2022.csv.gz',
    'play_by_play_2021.csv.gz', 'play_by_play_2020.csv.gz', 'play_by_play_2019.csv.gz',
    'play_by_play_2018.csv.gz', 'play_by_play_2017.csv.gz', 'play_by_play_2016.csv.gz',
    'play_by_play_2015.csv.gz', 'play_by_play_2014.csv.gz', 'play_by_play_2013.csv.gz',
    'play_by_play_2012.csv.gz', 'play_by_play_2011.csv.gz', 'play_by_play_2010.csv.gz',
    'play_by_play_2009.csv.gz', 'play_by_play_2008.csv.gz', 'play_by_play_2007.csv.gz',
    'play_by_play_2006.csv.gz', 'play_by_play_2005.csv.gz', 'play_by_play_2004.csv.gz',
    'play_by_play_2003.csv.gz', 'play_by_play_2002.csv.gz', 'play_by_play_2001.csv.gz',
    'play_by_play_2000.csv.gz', 'play_by_play_1999.csv.gz'
]

# Load the first file with header
df = pd.read_csv(csv_files[0], compression='gzip')

# Load subsequent files, skipping the header row
for csv_file in csv_files[1:]:
    print(f"Loading {csv_file}...")
    temp_df = pd.read_csv(csv_file, compression='gzip')
    df = pd.concat([df, temp_df], ignore_index=True)

# Connect to a DuckDB database file
con = duckdb.connect('nfl.duckdb')

# Save DataFrame to DuckDB
con.execute("DROP TABLE IF EXISTS play_by_play")
con.execute("CREATE TABLE play_by_play AS SELECT * FROM df")

con.close()