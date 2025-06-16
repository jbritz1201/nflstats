"""
API endpoints for NFL Quarterback statistics, including statistical qualification.
"""

from fastapi import FastAPI, HTTPException, Query
import duckdb
import pandas as pd
import os

app = FastAPI()

# Paths for SQL and DB
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQL_DIR = os.path.join(BASE_DIR, '..', 'sql')
DB_PATH = os.path.join(BASE_DIR, '..', 'nfl.duckdb')
QUERY_PATH = os.path.join(SQL_DIR, 'qbapi.sql')
QUALIFIED_PATH = os.path.join(SQL_DIR, 'qb_qualified_by_attempts.sql')

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
    df = con.execute(query, [f"%{qb_name}%"]).fetchdf()
    con.close()
    if df.empty:
        raise HTTPException(status_code=404, detail="Quarterback not found")
    return df.to_dict(orient="records")

@app.get("/api/qb_stats/all")
def get_all_qb_stats():
    """
    API endpoint to get stats for all quarterbacks (for league averages).
    """
    con = duckdb.connect(DB_PATH, read_only=True)
    query = load_query(QUERY_PATH)
    #df = con.execute(query, ['%']).fetchdf()
    df = con.execute(query, [f"%"]).fetchdf()
    con.close()
    if df.empty:
        raise HTTPException(status_code=404, detail="No quarterback stats found")
    return df.to_dict(orient="records")

@app.get("/api/stats/qualifier/qb/{min_attempts}")
def get_qb_qualifier(min_attempts: int):
    """
    API endpoint to get QBs who meet the minimum attempts threshold per season.
    """
    con = duckdb.connect(DB_PATH, read_only=True)
    query = load_query(QUALIFIED_PATH)
    df = con.execute(query, [min_attempts]).fetchdf()
    con.close()
    if df.empty:
        raise HTTPException(status_code=404, detail="No qualified quarterbacks found")
    return df.to_dict(orient="records")





