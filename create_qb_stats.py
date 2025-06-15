import duckdb
import pandas as pd

def load_query(filename):
    with open(filename, 'r') as f:
        return f.read()

def main():
    # Connect to the DuckDB database
    con = duckdb.connect('nfl.duckdb')

    # Load SQL query from external file
    query = load_query('qb_stats_query.sql')

    qb_df = con.execute(query).fetchdf()

    # Convert all NaN values to 0
    qb_df = qb_df.fillna(0)

    print(qb_df)

    con.close()

if __name__ == "__main__":
    main()