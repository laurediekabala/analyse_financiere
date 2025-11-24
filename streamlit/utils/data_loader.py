import pandas as pd
import streamlit as st
from pathlib import Path

@st.cache_data
def load_unemployment_data():

    try:
        # Si Streamlit est lancé depuis /streamlit, on remonte au dossier parent
        project_root = Path.cwd().parent
        data_path = project_root / "economics.csv"
        # DEBUG
        #st.write("CWD =", Path.cwd())
        #st.write("Chemin utilisé =", data_path)
        #st.write("Existe ? =", data_path.is_file())
        if not data_path.is_file():
            st.error(f"⚠️ Le fichier '{data_path}' n'a pas été trouvé !")
            return pd.DataFrame()
        df=pd.read_csv(data_path,index_col='date',parse_dates=True)
        df.drop("Unnamed: 0",axis=1,inplace=True)
        return df

    except Exception as e:
        st.error(f"❌ Erreur lors du chargement : {e}")
        return pd.DataFrame()

