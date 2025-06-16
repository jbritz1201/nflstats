import requests
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="NFL Quarterback Stats Explorer", layout="wide")

# Professional header
st.markdown(
    """
    <div style="text-align:center; margin-bottom: 2em;">
        <h1 style="color:#00BFFF;">🏈 NFL Quarterback Stats Explorer</h1>
    </div>
    """,
    unsafe_allow_html=True
)

qb_name = st.text_input(
    "Quarterback Name",
    help="Type a quarterback's name (partial or full) to see their stats.",
    placeholder="e.g. Tom Brady"
)

if qb_name:
    url = f"http://127.0.0.1:8000/api/qb_stats/{qb_name}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data:
            df = pd.DataFrame(data)
            # Format and shorten column names for readability
            col_rename = {
                'Attempts': 'Att',
                'Completions': 'Comp',
                'Touchdowns': 'TDs',
                'Interceptions': 'Ints',
                'Yards': 'Yds',
                'Fumbles Lost': 'Fum',
                'First Downs': '1st Downs'
            }
            # Normalize column names to title case with spaces
            df.columns = [col.replace('_', ' ').title() for col in df.columns]
            # Apply short names where appropriate
            df = df.rename(columns=col_rename)
            # Remove technical columns if present
            drop_cols = [col for col in df.columns if col.lower() in ['passer player id']]
            df = df.drop(columns=drop_cols, errors='ignore')
            # Sort by season and set season as string
            if 'Season' in df.columns:
                df['Season'] = df['Season'].astype(str) 
                df = df.sort_values('Season')
            # Get the actual player name from the returned data if available
            actual_name = None
            if 'Passer Player Name' in pd.DataFrame(data).columns and not pd.DataFrame(data).empty:
                actual_name = pd.DataFrame(data)['Passer Player Name'].iloc[0]
            # Layout: grid left, chart right
            col1, col2 = st.columns([2, 3], gap="large")
            with col1:
                # Brighter, visually distinct grid title with trophy icon and player name
                st.markdown(
                    f"""
                    <div style="font-size:2.2em; font-weight:900; color:#0078FF; margin-bottom:0.2em; text-align:left; letter-spacing:0.5px;">
                        🏆 QB Statistics by Season - {actual_name if actual_name else qb_name.title()}   
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                # Hide the first column (column 0) in the grid by default
                styled_df = (
                    df.iloc[:, 0:]  # Exclude the first column
                    .style.format(precision=0, thousands=",", na_rep="0")
                    .set_properties(**{'text-align': 'left'})
                )
                st.dataframe(
                    styled_df,
                    use_container_width=True,
                    height=min(500, 40 + 35 * len(df))
                )
            with col2:
                st.markdown(
                    f"""
                    <div style="font-size:2.2em; font-weight:900; color:#0078FF; margin-bottom:0.2em; text-align:left; letter-spacing:0.5px;">
                        📈 QB -  TDs vs. Ints
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                if {'Season', 'TDs', 'Ints'}.issubset(df.columns):
                    chart_data = df.set_index('Season')[['TDs', 'Ints']]
                    # Try to get league averages for the same seasons
                    try:
                        avg_url = f"http://127.0.0.1:8000/api/qb_stats/average_by_season"
                        avg_response = requests.get(avg_url)
                        avg_data = avg_response.json() if avg_response.status_code == 200 else []
                        avg_df = pd.DataFrame(avg_data)
                        avg_df.columns = [col.replace('_', ' ').title() for col in avg_df.columns]
                        avg_df['Season'] = avg_df['Season'].astype(str)
                        avg_df = avg_df[avg_df['Season'].isin(df['Season'])]
                        avg_df['Avg Touchdowns'] = pd.to_numeric(avg_df['Avg Touchdowns'], errors='coerce')
                        avg_df['Avg Interceptions'] = pd.to_numeric(avg_df['Avg Interceptions'], errors='coerce')
                        # Plot with matplotlib for custom styling
                        fig, ax = plt.subplots(figsize=(7, 4))
                        chart_data['TDs'].plot(ax=ax, marker='o', label='Player TDs', color='#2874A6')
                        chart_data['Ints'].plot(ax=ax, marker='o', label='Player INTs', color='#CA6F1E')
                        avg_df.set_index('Season')['Avg Touchdowns'].plot(ax=ax, color='red', linestyle='dotted', label='Avg TDs')
                        avg_df.set_index('Season')['Avg Interceptions'].plot(ax=ax, color='orange', linestyle='dotted', label='Avg INTs')
                        ax.set_title("TD(s) to Int(s) Year by Year", fontsize=14, color="#2E4053")
                        ax.set_ylabel("Count")
                        ax.set_xlabel("Season")
                        ax.legend()
                        ax.grid(alpha=0.3)
                        st.pyplot(fig)
                    except Exception:
                        st.line_chart(
                            data=chart_data,
                            use_container_width=True,
                            height=400
                        )
            
        else:
            st.info("No stats found for that quarterback.")
    except requests.exceptions.HTTPError:
        st.error("Quarterback not found.")
    except Exception as e:
        st.error(f"Error: {e}")