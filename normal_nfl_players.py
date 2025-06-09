# my_python_file.py

import pandas as pd

def main():
    # Load the Excel file into a DataFrame
    df = pd.read_excel('NFL_player_database.xlsx')
    # Create a new DataFrame with unique positions and a null alias column
    positions_df = pd.DataFrame({'position': df['position'].unique(), 'alias': [None]*df['position'].nunique()})
    # Set aliases for specific positions
    positions_df.loc[positions_df['position'].str.lower() == 'nose tackle', 'alias'] = 'DT'
    positions_df.loc[positions_df['position'].str.lower() == 'end', 'alias'] = 'DE'
    positions_df.loc[positions_df['position'].str.lower() == 'blocking back', 'alias'] = 'FB'
    positions_df.loc[positions_df['position'].str.lower() == 'running back', 'alias'] = 'RB'
    positions_df.loc[positions_df['position'].str.lower() == 'kicker', 'alias'] = 'KI'
    positions_df.loc[positions_df['position'].str.lower() == 'wide reciever', 'alias'] = 'WR'
    positions_df.loc[positions_df['position'].str.lower() == 'halfback', 'alias'] = 'RB'
    positions_df.loc[positions_df['position'].str.lower() == 'defensive end', 'alias'] = 'DE'
    positions_df.loc[positions_df['position'].str.lower() == 'safety', 'alias'] = 'S'
    positions_df.loc[positions_df['position'].str.lower() == 'defensive back', 'alias'] = 'DB'
    positions_df.loc[positions_df['position'].str.lower() == 'line backer', 'alias'] = 'LB'
    positions_df.loc[positions_df['position'].str.lower() == 'tailback', 'alias'] = 'RB'
    positions_df.loc[positions_df['position'].str.lower() == 'offensive tackle', 'alias'] = 'OT'
    positions_df.loc[positions_df['position'].str.lower() == 'offensive guard', 'alias'] = 'OG'
    positions_df.loc[positions_df['position'].str.lower() == 'tight end', 'alias'] = 'TE'
    positions_df.loc[positions_df['position'].str.lower() == 'fullback', 'alias'] = 'FB'
    positions_df.loc[positions_df['position'].str.lower() == 'linebacker', 'alias'] = 'LB'
    positions_df.loc[positions_df['position'].str.lower() == 'defensive tackle', 'alias'] = 'DT'
    positions_df.loc[positions_df['position'].str.lower() == 'offensive lineman', 'alias'] = 'OL'
    positions_df.loc[positions_df['position'].str.lower() == 'defensive lineman', 'alias'] = 'DL'
    positions_df.loc[positions_df['position'].str.lower() == 'defensive tackle', 'alias'] = 'DT'
    positions_df.loc[positions_df['position'].str.lower() == 'offensive tackle', 'alias'] = 'OT'
    positions_df.loc[positions_df['position'].str.lower() == 'offensive lineman', 'alias'] = 'OL'
    positions_df.loc[positions_df['position'].str.lower() == 'linebackers', 'alias'] = 'LB'
    positions_df.loc[positions_df['position'].str.lower() == 'defensive backs', 'alias'] = 'DB'
    positions_df.loc[positions_df['position'].str.lower() == 'defensive linemen', 'alias'] = 'DL'
    positions_df.loc[positions_df['position'].str.lower() == 'offensive linemen', 'alias'] = 'OL'
    positions_df.loc[positions_df['position'].str.lower() == 'guard', 'alias'] = 'OG'
    positions_df.loc[positions_df['position'].str.lower() == 'quarterback', 'alias'] = 'QB'
    positions_df.loc[positions_df['position'].str.lower() == 'punter', 'alias'] = 'P'
    positions_df.loc[positions_df['position'].str.lower() == 'place kicker', 'alias'] = 'KI'
    positions_df.loc[positions_df['position'].str.lower() == 'cornerback', 'alias'] = 'CB'
    positions_df.loc[positions_df['position'].str.lower() == 'long snapper', 'alias'] = 'LS'
    positions_df.loc[positions_df['position'].str.lower() == 'special teams', 'alias'] = 'ST'
    positions_df.loc[positions_df['position'].str.lower() == 'special teams player', 'alias'] = 'ST'
    positions_df.loc[positions_df['position'].str.lower() == 'wide receiver', 'alias'] = 'WR'
    positions_df.loc[positions_df['position'].str.lower() == 'tackle', 'alias'] = 'OT'
    positions_df.loc[positions_df['position'].str.lower() == 'outside linebacker', 'alias'] = 'OLB'
    positions_df.loc[positions_df['position'].str.lower() == 'back', 'alias'] = 'RB'
    positions_df.loc[positions_df['position'].str.lower() == 'wingback', 'alias'] = 'RB'
    positions_df.loc[positions_df['position'].str.lower() == 'center', 'alias'] = 'C'   
    positions_df.loc[positions_df['position'].str.lower() == 'free safety', 'alias'] = 'FS'
    positions_df.loc[positions_df['position'].str.lower() == 'inside linebcker', 'alias'] = 'ILB'
    positions_df.loc[positions_df['position'].str.lower() == 'flanker', 'alias'] = 'WR'
    positions_df.loc[positions_df['position'].str.lower() == 'defensive guard', 'alias'] = 'DT'
    positions_df.loc[positions_df['position'].str.lower() == 'right guard', 'alias'] = 'OG'
    positions_df.loc[positions_df['position'].str.lower() == 'left guard', 'alias'] = 'OG'
    positions_df.loc[positions_df['position'].str.lower() == 'split end', 'alias'] = 'TE'
    positions_df.loc[positions_df['position'].str.lower() == 'slot receiver', 'alias'] = 'WR'
    # Remove duplicate positions
    positions_df = positions_df.drop_duplicates(subset=['position'])
    print(positions_df)

    # Map aliases from positions_df to df
    alias_map = dict(zip(positions_df['position'].str.lower(), positions_df['alias']))
    # Add a new column 'modern_position' with the alias if it exists, else keep the original position
    df['modern_position'] = df['position'].apply(lambda x: alias_map.get(str(x).lower(), x))
    print(df)
    # Loop through distinct modern positions and show all players at each modern position
    for position in df['modern_position'].unique():
        print(f'\nPlayers at modern position: {position}')
        print(df[df['modern_position'] == position])
  

if __name__ == "__main__":
    main()
