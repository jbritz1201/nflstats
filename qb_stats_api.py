from fastapi import FastAPI, HTTPException
import duckdb
import pandas as pd

app = FastAPI()

DB_PATH = "nfl.duckdb"

@app.get("/qb_stats/{qb_name}")
def get_qb_stats(qb_name: str):
    """
    API endpoint to get stats for a given quarterback name (case-insensitive, partial match).
    """
    con = duckdb.connect(DB_PATH, read_only=True)
    query = """
        SELECT *
        FROM qb_stats
        WHERE LOWER(passer_player_name) LIKE LOWER(?)
        ORDER BY season
    """
    # Use wildcards for partial matching
    df = con.execute(query, [f"%{qb_name}%"]).fetchdf()
    con.close()
    if df.empty:
        raise HTTPException(status_code=404, detail="Quarterback not found")
    return df.to_dict(orient="records")