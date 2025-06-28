import duckdb
import pandas as pd
import os

def load_query(filename):
    with open(filename, 'r') as f:
        return f.read()

def main():
    # Use absolute path for the SQL file in the sql directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sql_path = os.path.join(base_dir, 'sql', 'qb_stats_query.sql')
    db_path = os.path.join(base_dir, 'nfl.duckdb')

    # Connect to the DuckDB database
    con = duckdb.connect(db_path)

    # Load SQL query from external file
    query = load_query(sql_path)

    # Create qb_stats table from the query
    con.execute("DROP TABLE IF EXISTS passer_stats")
    con.execute(f"CREATE TABLE passer_stats AS {query}")

    # Optionally, load and print the table to verify
    qb_df = con.execute("SELECT * FROM passer_stats").fetchdf()
    qb_df = qb_df.fillna(0)
    print(qb_df)

    con.close()

if __name__ == "__main__":
    main()