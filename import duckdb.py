import duckdb
import pandas as pd

years = range(2024, 1998, -1)
# List of compressed CSV files to load (updated directory structure)
csv_files = [f"data/raw/nfl/play_by_play_{year}.csv.gz" for year in years]

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