# my_python_file.py

import pandas as pd
import sqlite3

def load_data(filename):
    """Load the Excel file into a DataFrame."""
    return pd.read_excel(filename)

def build_positions_df(df):
    """Create a DataFrame with unique positions and their aliases."""
    positions = df['position'].dropna().unique()
    positions_df = pd.DataFrame({'position': positions, 'alias': [None]*len(positions)})
    # Define mapping of positions to aliases
    alias_map = {
        'nose tackle': 'DT', 'end': 'DE', 'blocking back': 'FB', 'running back': 'RB',
        'kicker': 'KI', 'wide reciever': 'WR', 'halfback': 'RB', 'defensive end': 'DE',
        'safety': 'S', 'defensive back': 'DB', 'line backer': 'LB', 'tailback': 'RB',
        'offensive tackle': 'OT', 'offensive guard': 'OG', 'tight end': 'TE', 'fullback': 'FB',
        'linebacker': 'LB', 'defensive tackle': 'DT', 'offensive lineman': 'OL', 'defensive lineman': 'DL',
        'linebackers': 'LB', 'defensive backs': 'DB', 'defensive linemen': 'DL', 'offensive linemen': 'OL',
        'guard': 'OG', 'quarterback': 'QB', 'punter': 'P', 'place kicker': 'KI', 'cornerback': 'CB',
        'long snapper': 'LS', 'special teams': 'ST', 'special teams player': 'ST', 'wide receiver': 'WR',
        'tackle': 'OT', 'outside linebacker': 'OLB', 'back': 'RB', 'wingback': 'RB', 'center': 'C',
        'free safety': 'FS', 'inside linebcker': 'ILB', 'flanker': 'WR', 'defensive guard': 'DT',
        'right guard': 'OG', 'left guard': 'OG', 'split end': 'TE', 'slot receiver': 'WR'
    }
    positions_df['alias'] = positions_df['position'].str.lower().map(alias_map)
    positions_df = positions_df.drop_duplicates(subset=['position'])
    return positions_df

def add_modern_position(df, positions_df):
    """Add a 'modern_position' column to df using the alias from positions_df."""
    alias_map = dict(zip(positions_df['position'].str.lower(), positions_df['alias']))
    df['modern_position'] = df['position'].apply(lambda x: alias_map.get(str(x).lower(), x))
    return df

def print_players_by_modern_position(df):
    """Print all players grouped by modern_position."""
    for position in df['modern_position'].dropna().unique():
        print(f'\nPlayers at modern position: {position}')
        print(df[df['modern_position'] == position])

def run_query(query):
    """Run a SQL query on the nfl_players.db SQLite database and print the result as a DataFrame."""
    conn = sqlite3.connect('nfl_players.db')
    result = pd.read_sql_query(query, conn)
    conn.close()
    print(result)

def main():
    df = load_data('NFL_player_database.xlsx')
    positions_df = build_positions_df(df)
    print(positions_df)
    df = add_modern_position(df, positions_df)
    print(df)
    print_players_by_modern_position(df)
    # Example SQL queries
    print("\nExample: First 5 players from the database:")
    run_query("SELECT * FROM players LIMIT 5;")
    print("\nExample: Distinct positions in the database:")
    run_query("SELECT DISTINCT position FROM players;")

if __name__ == "__main__":
    main()
