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

    # Create qb_stats table from the query
    con.execute("DROP TABLE IF EXISTS qb_stats")
    con.execute(f"CREATE TABLE qb_stats AS {query}")

    # Optionally, load and print the table to verify
    qb_df = con.execute("SELECT * FROM qb_stats").fetchdf()
    qb_df = qb_df.fillna(0)
    print(qb_df)

    con.close()

if __name__ == "__main__":
    main()