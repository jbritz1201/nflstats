import duckdb
import os

def load_query(filename):
    with open(filename, 'r') as f:
        return f.read()

def main():
    # Set up paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sql_path = os.path.join(base_dir, 'sql', 'qb_qualified_by_attempts.sql')
    db_path = os.path.join(base_dir, 'nfl.duckdb')

    # Load SQL query from file
    query = load_query(sql_path)

    # Connect to DuckDB and create the table
    con = duckdb.connect(db_path)
    con.execute("DROP TABLE IF EXISTS qb_averages_by_season")
    con.execute(f"CREATE TABLE qb_averages_by_season AS {query}")
    # Optionally print the table to verify
    df = con.execute("SELECT * FROM qb_averages_by_season").fetchdf()
    print(df)
    con.close()

if __name__ == "__main__":
    main()