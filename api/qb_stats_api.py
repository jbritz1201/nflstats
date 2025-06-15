from fastapi import FastAPI, HTTPException
import duckdb
import pandas as pd
import os

app = FastAPI()

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'nfl.duckdb')
QUERY_PATH = os.path.join(os.path.dirname(__file__), '..', 'sql', 'qbapi.sql')

def load_query(filename):
    with open(filename, 'r') as f:
        return f.read()

@app.get("/api/qb_stats/{qb_name}")
def get_qb_stats(qb_name: str):
    """
    API endpoint to get stats for a given quarterback name (case-insensitive, partial match).
    """
    con = duckdb.connect(DB_PATH, read_only=True)
    query = load_query(QUERY_PATH)
    # Use wildcards for partial matching
    df = con.execute(query, [f"%{qb_name}%"]).fetchdf()
    con.close()
    if df.empty:
        raise HTTPException(status_code=404, detail="Quarterback not found")
    return df.to_dict(orient="records")