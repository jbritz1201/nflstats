import duckdb
import pandas as pd

# Connect to DuckDB and load the nfl_game_details table
con = duckdb.connect('nfl.duckdb')
df = con.execute("SELECT * FROM nfl_game_details").fetchdf()

# Calculate team records (wins, losses, ties) for each team
def get_team_records(df):
    teams = pd.unique(df[['home_team', 'away_team']].values.ravel('K'))
    records = []
    for team in teams:
        home_games = df[df['home_team'] == team]
        away_games = df[df['away_team'] == team]
        home_wins = (home_games['winning_team'] == 'home').sum()
        home_losses = (home_games['winning_team'] == 'away').sum()
        home_ties = ((home_games['winning_team'].isna()) | (home_games['winning_team'] == 'TIE')).sum()
        away_wins = (away_games['winning_team'] == 'away').sum()
        away_losses = (away_games['winning_team'] == 'home').sum()
        away_ties = ((away_games['winning_team'].isna()) | (away_games['winning_team'] == 'TIE')).sum()
        wins = home_wins + away_wins
        losses = home_losses + away_losses
        ties = home_ties + away_ties

        # Regular season only
        reg_home_games = home_games[home_games['season_type'] == 'REG']
        reg_away_games = away_games[away_games['season_type'] == 'REG']
        reg_home_wins = (reg_home_games['winning_team'] == 'home').sum()
        reg_home_losses = (reg_home_games['winning_team'] == 'away').sum()
        reg_home_ties = ((reg_home_games['winning_team'].isna()) | (reg_home_games['winning_team'] == 'TIE')).sum()
        reg_away_wins = (reg_away_games['winning_team'] == 'away').sum()
        reg_away_losses = (reg_away_games['winning_team'] == 'home').sum()
        reg_away_ties = ((reg_away_games['winning_team'].isna()) | (reg_away_games['winning_team'] == 'TIE')).sum()
        reg_season_wins = reg_home_wins + reg_away_wins
        reg_season_losses = reg_home_losses + reg_away_losses
        reg_season_ties = reg_home_ties + reg_away_ties

        # Playoff only
        playoff_home_games = home_games[home_games['season_type'] == 'POST']
        playoff_away_games = away_games[away_games['season_type'] == 'POST']
        playoff_home_wins = (playoff_home_games['winning_team'] == 'home').sum()
        playoff_home_losses = (playoff_home_games['winning_team'] == 'away').sum()
        playoff_away_wins = (playoff_away_games['winning_team'] == 'away').sum()
        playoff_away_losses = (playoff_away_games['winning_team'] == 'home').sum()
        playoff_wins = playoff_home_wins + playoff_away_wins
        playoff_losses = playoff_home_losses + playoff_away_losses

        records.append({
            'team': team,
            'wins': wins,
            'losses': losses,
            'ties': ties,
            'home_wins': home_wins,
            'home_losses': home_losses,
            'home_ties': home_ties,
            'away_wins': away_wins,
            'away_losses': away_losses,
            'away_ties': away_ties,
            'reg_season_wins': reg_season_wins,
            'reg_season_losses': reg_season_losses,
            'reg_season_ties': reg_season_ties,
            'reg_season_home_wins': reg_home_wins,
            'reg_season_home_losses': reg_home_losses,
            'reg_season_home_ties': reg_home_ties,
            'reg_season_away_wins': reg_away_wins,
            'reg_season_away_losses': reg_away_losses,
            'reg_season_away_ties': reg_away_ties,
            'playoff_wins': playoff_wins,
            'playoff_losses': playoff_losses,
            'playoff_home_wins': playoff_home_wins,
            'playoff_home_losses': playoff_home_losses,
            'playoff_away_wins': playoff_away_wins,
            'playoff_away_losses': playoff_away_losses
        })
    return pd.DataFrame(records)

team_records_df = get_team_records(df)

# Find Super Bowl winners by season (max old_game_id for POST season_type)
super_bowl_winners = (
    df[df['season_type'] == 'POST']
    .loc[lambda d: d.groupby('season')['old_game_id'].transform('max') == d['old_game_id']]
    .reset_index(drop=True)
)

# Assign super_bowl_winner as the winning_team_name for each Super Bowl
super_bowl_winners['super_bowl_winner'] = super_bowl_winners['winning_team_name']

# Count Super Bowl wins by team
super_bowl_counts = (
    super_bowl_winners['super_bowl_winner']
    .value_counts()
    .rename_axis('team')
    .reset_index(name='super_bowl_wins')
)

# Determine Super Bowl losers
def get_super_bowl_loser(row):
    if row['winning_team'] == 'home':
        return row['away_team']
    elif row['winning_team'] == 'away':
        return row['home_team']
    else:
        return None

super_bowl_winners['super_bowl_loser'] = super_bowl_winners.apply(get_super_bowl_loser, axis=1)

# Count Super Bowl losses by team
super_bowl_loser_counts = (
    super_bowl_winners['super_bowl_loser']
    .value_counts()
    .rename_axis('team')
    .reset_index(name='super_bowl_losses')
)

# Merge Super Bowl wins and losses into a single DataFrame
super_bowl_summary = pd.merge(
    super_bowl_counts,
    super_bowl_loser_counts,
    on='team',
    how='outer'
).fillna(0)

# Calculate conference championships before merging into team_records_df
super_bowl_summary['super_bowl_wins'] = super_bowl_summary['super_bowl_wins'].astype(int)
super_bowl_summary['super_bowl_losses'] = super_bowl_summary['super_bowl_losses'].astype(int)
super_bowl_summary['conference_championships'] = (
    super_bowl_summary['super_bowl_wins'] + super_bowl_summary['super_bowl_losses']
)

# Reorder columns as requested
super_bowl_summary = super_bowl_summary[
    ['team', 'conference_championships', 'super_bowl_wins', 'super_bowl_losses']
]

# Merge into team_records_df
team_records_df = team_records_df.merge(super_bowl_summary, on='team', how='left')
team_records_df[['conference_championships', 'super_bowl_wins', 'super_bowl_losses']] = (
    team_records_df[['conference_championships', 'super_bowl_wins', 'super_bowl_losses']].fillna(0).astype(int)
)

# Save the team records to DuckDB
con.execute("DROP TABLE IF EXISTS team_records")
con.execute("CREATE TABLE team_records AS SELECT * FROM team_records_df")

# Preview the new table
result = con.execute("SELECT * FROM team_records ORDER BY team LIMIT 10").fetchdf()
print(result)

con.close()