import duckdb
import os

def load_query(filename):
    with open(filename, 'r') as f:
        return f.read()

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sql_path = os.path.join(base_dir, 'sql', 'receiving_stats.sql')
    db_path = os.path.join(base_dir, 'nfl.duckdb')

    query = load_query(sql_path)

    con = duckdb.connect(db_path)
    con.execute("DROP TABLE IF EXISTS receiving_stats")
    con.execute(f"CREATE TABLE receiving_stats AS {query}")
    # Optionally print the first few rows to verify
    df = con.execute("SELECT * FROM receiving_stats").fetchdf()
    print(df)
    con.close()

if __name__ == "__main__":
    main()