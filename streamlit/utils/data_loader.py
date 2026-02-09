import pandas as pd
import streamlit as st
from pathlib import Path

@st.cache_data
def load_unemployment_data():

    try:
        BASE_DIR = Path(__file__).resolve().parent.parent.parent
        data_path = BASE_DIR / "economics.csv"

        if not data_path.is_file():
            st.error(f"⚠️ Fichier introuvable : {data_path}")
            return pd.DataFrame()

        df = pd.read_csv(
            data_path,
            index_col="date",
            parse_dates=True
        )

        if "Unnamed: 0" in df.columns:
            df.drop(columns=["Unnamed: 0"], inplace=True)

        return df

    except Exception as e:
        st.error(f"❌ Erreur lors du chargement : {e}")
        return pd.DataFrame()
