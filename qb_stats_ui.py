import requests
import streamlit as st
import pandas as pd

st.title("Quarterback Stats Lookup")

qb_name = st.text_input("Enter QB Name (partial or full):")

if qb_name:
    url = f"http://127.0.0.1:8000/qb_stats/{qb_name}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data:
            df = pd.DataFrame(data)
            st.dataframe(df)
        else:
            st.info("No stats found for that quarterback.")
    except requests.exceptions.HTTPError as e:
        st.error("Quarterback not found.")
    except Exception as e:
        st.error(f"Error: {e}")