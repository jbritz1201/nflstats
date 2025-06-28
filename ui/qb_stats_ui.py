import requests
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set Streamlit theme to dark
st.set_page_config(page_title="NFL Quarterback Stats Explorer", layout="wide", initial_sidebar_state="auto")
st.markdown(
    """
    <style>
        body, .stApp { background-color: #18191A; color: #FFFFFF; }
        .stDataFrame { background-color: #23272F; }
        .css-1d391kg { background-color: #23272F; }
    </style>
    """,
    unsafe_allow_html=True
)

# Professional header
st.markdown(
    """
    <div style="text-align:center; margin-bottom: 2em;">
        <h1 style="color:#00BFFF;">🏈 NFL Quarterback Stats Explorer</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Get all distinct QB names from the API
@st.cache_data(show_spinner=False)
def get_all_qb_names():
    url = "http://127.0.0.1:8000/api/qb/list/all"
    response = requests.get(url)
    if response.status_code == 200:
        return sorted(response.json())
    return []

qb_names_list = get_all_qb_names()

qb_name = st.selectbox(
    "Select Quarterback",
    qb_names_list,
    help="Choose a quarterback to see their stats."
)

if qb_name:
    url = f"http://127.0.0.1:8000/api/qb/stats/{qb_name}"
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
            col1, col2 = st.columns([4, 3], gap="large")
            with col1:
                # Brighter, visually distinct grid title with trophy icon and player name
                st.markdown(
                    f"""
                    <div style="font-size:2.2em; font-weight:900; color:#00BFFF; margin-bottom:0.2em; text-align:left; letter-spacing:0.5px;">
                        🏆 QB Statistics by Season - {actual_name if actual_name else qb_name.title()}   
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                # Set the desired column order for the grid
                desired_order = [
                    'Season', 'Games', 'Att', 'Comp', 'TDs', 'Ints', 'Yds', 'Fum', 'Sacks', '1st Downs'
                ]
                # Only include columns that exist in the DataFrame
                display_cols = [col for col in desired_order if col in df.columns]
                styled_df = (
                    df[display_cols]
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
                    <div style="font-size:2.2em; font-weight:900; color:#00BFFF; margin-bottom:0.2em; text-align:left; letter-spacing:0.5px;">
                        📈 QB -  TDs vs. Ints
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                if {'Season', 'TDs', 'Ints'}.issubset(df.columns):
                    chart_data = df.set_index('Season')[['TDs', 'Ints']]
                    try:
                        avg_url = f"http://127.0.0.1:8000/api/qb/stats/avg/all"
                        avg_response = requests.get(avg_url)
                        avg_data = avg_response.json() if avg_response.status_code == 200 else []
                        avg_df = pd.DataFrame(avg_data)
                        avg_df.columns = [col.replace('_', ' ').title() for col in avg_df.columns]
                        avg_df['Season'] = avg_df['Season'].astype(str)
                        avg_df = avg_df[avg_df['Season'].isin(df['Season'])]

                        # Use dark theme for matplotlib
                        plt.style.use('dark_background')
                        fig, ax = plt.subplots(figsize=(7, 4))
                        y_min = min(
                            chart_data.min().min(),
                            avg_df['Avg Td'].min() if 'Avg Td' in avg_df.columns else float('inf'),
                            avg_df['Avg Int'].min() if 'Avg Int' in avg_df.columns else float('inf')
                        )
                        y_max = max(
                            chart_data.max().max(),
                            avg_df['Avg Td'].max() if 'Avg Td' in avg_df.columns else float('-inf'),
                            avg_df['Avg Int'].max() if 'Avg Int' in avg_df.columns else float('-inf')
                        )
                        chart_data['TDs'].plot(ax=ax, label='Player TDs', color='#2874A6')
                        chart_data['Ints'].plot(ax=ax, label='Player INTs', color='#CA6F1E')
                        if 'Avg Td' in avg_df.columns and 'Avg Int' in avg_df.columns:
                            avg_df.set_index('Season')['Avg Td'].plot(ax=ax, color='red', linestyle='dotted', label='Avg TDs')
                            avg_df.set_index('Season')['Avg Int'].plot(ax=ax, color='orange', linestyle='dotted', label='Avg INTs')
                        ax.set_title("TD(s) to Int(s) Year by Year", fontsize=14, color="#00BFFF")
                        ax.set_ylabel("Count", color="#FFFFFF")
                        ax.set_xlabel("Season", color="#FFFFFF")
                        ax.set_ylim(y_min, y_max)
                        ax.legend(fontsize=10)
                        ax.grid(alpha=0.3)
                        ax.tick_params(colors='#FFFFFF')
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