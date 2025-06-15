import requests
import streamlit as st
import pandas as pd

st.title("Quarterback Stats Lookup")

qb_name = st.text_input("Enter QB Name (partial or full):")

if qb_name:
    # Updated API URL to reflect new location under /api/
    url = f"http://127.0.0.1:8000/api/qb_stats/{qb_name}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data:
            df = pd.DataFrame(data)
            st.dataframe(df)
            # Plot touchdowns and interceptions by year if data is available
            if 'season' in df.columns and 'touchdowns' in df.columns and 'interceptions' in df.columns:
                df['season'] = df['season'].astype(str)  # Treat year as string
                df_sorted = df.sort_values('season')
                chart_data = df_sorted.set_index('season')[['touchdowns', 'interceptions']]
                st.line_chart(
                    data=chart_data,
                    use_container_width=True
                )
                st.markdown("#### TD(s) to Int(s) Year by Year")
        else:
            st.info("No stats found for that quarterback.")
    except requests.exceptions.HTTPError as e:
        st.error("Quarterback not found.")
    except Exception as e:
        st.error(f"Error: {e}")