import duckdb
import os

def load_query(filename):
    with open(filename, 'r') as f:
        return f.read()

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sql_path = os.path.join(base_dir, 'sql', 'rushing_stats.sql')
    db_path = os.path.join(base_dir, 'nfl.duckdb')

    query = load_query(sql_path)

    con = duckdb.connect(db_path)
    con.execute("DROP TABLE IF EXISTS rushing_stats")
    con.execute(f"CREATE TABLE rushing_stats AS {query}")
    # Optionally print the table to verify
    df = con.execute("SELECT * FROM rushing_stats LIMIT 5").fetchdf()
    print(df)
    con.close()

if __name__ == "__main__":
    main()