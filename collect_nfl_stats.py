import pandas as pd
import sqlite3
import glob

def main():
    # Load all .xlsx files in the current directory into a single DataFrame
    excel_files = glob.glob('2014stats*.xlsx')
    if not excel_files:
        print("No Excel files found matching '2014stats.xlsx'.")
        return
    df_list = [pd.read_excel(file) for file in excel_files]
    df = pd.concat(df_list, ignore_index=True)
    print(df)


#     # This script is intentionally left blank as per the request.
#     pass
# #     positions_df = positions_df.drop_duplicates(subset=['position'])
# #     # Add a new column 'modern_position' to the original DataFrame

# # collect_nfl_stats.py
# # (This file has been intentionally left blank.)
