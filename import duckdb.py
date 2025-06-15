import duckdb
import pandas as pd

# Load CSV into a pandas DataFrame
df = pd.read_csv('play_by_play_2024.csv')

# Connect to a DuckDB database file (or use ':memory:' for in-memory)
con = duckdb.connect('nfl.duckdb')

# Save DataFrame to DuckDB
con.execute("CREATE TABLE play_by_play_2024 AS SELECT * FROM df")

# Query DuckDB
result = con.execute("SELECT * FROM play_by_play_2024 LIMIT 5").fetchdf()
print(result)

con.close()