import duckdb
import pandas as pd

# Load the play_by_play table into a DataFrame from DuckDB
con = duckdb.connect('nfl.duckdb')
df = con.execute("SELECT * FROM play_by_play").fetchdf()

# Select the specified columns and drop duplicates to mimic GROUP BY ALL
game_details_df = df[
    [
        "game_id", "old_game_id", "home_team", "away_team", "week", "game_date",
        "season_type", "away_score", "home_score", "location", "total", "result",
        "spread_line", "total_line", "div_game", "start_time", "stadium", 
        "weather", "roof", "surface", "temp", "wind", "home_coach", "away_coach", 
        "stadium_id", "game_stadium"
    ]
].drop_duplicates().sort_values("old_game_id")

# Add winning_team column
def determine_winner(row):
    if pd.isna(row['home_score']) or pd.isna(row['away_score']):
        return None
    if row['home_score'] > row['away_score']:
        return 'home'
    elif row['home_score'] < row['away_score']:
        return 'away'
    else:
        return None

game_details_df['winning_team'] = game_details_df.apply(determine_winner, axis=1)

def get_winning_team_name(row):
    if row['winning_team'] == 'away':
        return row['away_team']
    elif row['winning_team'] == 'home':
        return row['home_team']
    else:
        return 'TIE'

game_details_df['winning_team_name'] = game_details_df.apply(get_winning_team_name, axis=1)

# Add season column by extracting the first 4 characters of game_id
game_details_df['season'] = game_details_df['game_id'].astype(str).str[:4]

# Save the DataFrame back to DuckDB as nfl_game_details
con.execute("DROP TABLE IF EXISTS nfl_game_details")
con.execute("CREATE TABLE nfl_game_details AS SELECT * FROM game_details_df")

# Preview the new table
result = con.execute("SELECT * FROM nfl_game_details LIMIT 5").fetchdf()
print(result)

con.close()