import streamlit as st
import pandas as pd
from utils.data_loader import load_unemployment_data
import os
from pathlib import Path
CURRENT_DIR = Path(__file__).resolve().parent
IMAGE_PATH = CURRENT_DIR.parent / "images" / "ld.jpg"

# Vérifier si l'utilisateur est connecté
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Veuillez vous connecter pour accéder à cette page.")
    st.stop()

st.set_page_config(
    page_title="Accueil",
    page_icon="🏠",
    layout="wide"
)

st.markdown("<h1 class='welcome-header'>Bienvenue sur notre application dédiée au chômage aux USA !</h1>", unsafe_allow_html=True)
st.markdown("<p class='welcome-subheader'>Explorez les données historiques, les analyses descriptives et les prévisions de nombre des chômeurs entre 1957 et 2015 aux États-Unis.</p>", unsafe_allow_html=True)
st.image(str(IMAGE_PATH), use_container_width=True)

st.markdown("""
<div style='text-align: justify; margin-top: 2em; font-size: 1.1em;'>
    Cette application est conçue pour fournir une vue d'ensemble complète et interactive de nbr des chômeurs aux États-Unis.
    En tant qu'outil essentiel pour les économistes, les analystes de données et les décideurs, elle permet de visualiser les tendances historiques,
    d'effectuer des analyses descriptives approfondies et de consulter des prévisions basées sur des modèles de Machine Learning avancés (LSTM).
    Naviguez à travers les différentes sections pour découvrir des informations clés et des projections futures.
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='center-button'>", unsafe_allow_html=True)
if st.button("Afficher le Dataset Brute"):
    st.subheader("Dataset du Taux de Chômage aux USA")
    df = load_unemployment_data()
    st.dataframe(df,use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)