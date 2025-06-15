# my_python_file.py
import pandas as pd

def main():
    # Load play_by_play_2024.csv into a DataFrame
    try:
        df = pd.read_csv('play_by_play_2024.csv')
        print(df.head())  # Display the first few rows
    except FileNotFoundError:
        print("The file 'play_by_play_2024.csv' was not found.")

if __name__ == "__main__":
    main()
import pandas as pd
import sqlite3



def main():
    # Load play_by_play_2024.csv into a DataFrame
    try:
        play_by_play_df = pd.read_csv('play_by_play_2024.csv')
        print(play_by_play_df.head())  # Display the first few rows
    except FileNotFoundError:
        print("The file 'play_by_play_2024.csv' was not found.")


if __name__ == "__main__":
    main()
