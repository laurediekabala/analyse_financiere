import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_unemployment_data
from statsmodels.tsa.seasonal import seasonal_decompose
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------
# Authentification
# ---------------------------------------------------------------------
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Veuillez vous connecter pour accéder à cette page.")
    st.stop()

st.set_page_config(
    page_title="Analyse Descriptive",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Analyse Descriptive des Indicateurs Économiques (USA)")
st.markdown("Analysez les tendances, la saisonnalité et les structures statistiques.")

# ---------------------------------------------------------------------
# Chargement des données
# ---------------------------------------------------------------------
df = load_unemployment_data()

if df.empty:
    st.error("Erreur : impossible de charger les données.")
    st.stop()

# ---------------------------------------------------------------------
# Variables existantes dans le dataset
# ---------------------------------------------------------------------
available_vars = df.columns.tolist()

st.sidebar.subheader("Sélection de la variable")
selected_var = st.sidebar.selectbox("Choisissez une variable :", available_vars)

# ---------------------------------------------------------------------
# 1) Statistiques générales
# ---------------------------------------------------------------------
st.subheader("Statistiques Générales")
st.dataframe(df[selected_var].describe().to_frame())

# ---------------------------------------------------------------------
# 2) Graphique original
# ---------------------------------------------------------------------
st.subheader("Évolution Temporelle")
fig = px.line(
    df,
    x=df.index,
    y=selected_var,
    title=f"Série Temporelle : {selected_var}",
    labels={"x": "Date", selected_var: selected_var},
    template="plotly_white"
)
fig.update_traces(line_color='#00796b', line_width=2)
fig.update_layout(hovermode="x unified")
st.plotly_chart(fig, use_container_width=True)
# Analyse par année ou autre agrégation st.subheader("Analyse Annuelle") 
df['year'] = df.index.year 
df_yearly_avg = df.groupby('year')[selected_var].mean().reset_index() 
fig_bar = px.bar(df_yearly_avg, x='year', y=selected_var, title=f'{selected_var} Annuel Moyen aux USA', labels={'year': 'Année', f'{selected_var}': f'{selected_var} Annuel Moyen (%)'}, template="plotly_white", color_discrete_sequence=px.colors.sequential.Teal_r) 
st.plotly_chart(fig_bar, use_container_width=True)
# moyenne mobile
st.subheader("Moyenne Mobile")
window = st.slider("Taille de la fenêtre (mois)", 3, 24, 12)

df[f"{selected_var}_MA"] = df[selected_var].rolling(window=window).mean()

fig_ma = px.line(
    df,
    x=df.index,
    y=[selected_var, f"{selected_var}_MA"],
    title=f"Moyenne Mobile ({window} mois) — {selected_var}",
    labels={"x": "Date"},
    template="plotly_white"
)
fig_ma.update_layout(hovermode="x unified")
st.plotly_chart(fig_ma, use_container_width=True)

# ---------------------------------------------------------------------
# 4) Matrice de corrélation
# ---------------------------------------------------------------------
st.subheader("Matrice de Corrélation")
if st.button("Afficher la matrice de corrélation"):
    corr = df.corr()

    st.dataframe(
        corr.style.background_gradient(cmap="coolwarm").format(precision=2)
    )

# ---------------------------------------------------------------------
# 5) Décomposition saisonnière
# ---------------------------------------------------------------------
st.subheader(f"Décomposition Saisonnière — {selected_var}")

if st.button("Afficher la décomposition saisonnière"):
    try:
        ts = df[selected_var].dropna()

        decomposition = seasonal_decompose(ts, model="additive", period=12)

        fig_dec, axes = plt.subplots(4, 1, figsize=(14, 10), sharex=True)

        decomposition.observed.plot(ax=axes[0], title="Série Observée", linewidth=2)
        axes[0].grid(True)

        decomposition.trend.plot(ax=axes[1], title="Tendance (Trend)", linewidth=2, color="#00838f")
        axes[1].grid(True)

        decomposition.seasonal.plot(ax=axes[2], title="Saisonnalité (Seasonal)", linewidth=2, color="#00695c")
        axes[2].grid(True)

        decomposition.resid.plot(ax=axes[3], title="Résidus (Residual)", linewidth=2, color="#ff7043")
        axes[3].grid(True)

        plt.tight_layout()
        st.pyplot(fig_dec)

    except Exception as e:
        st.error(f"Erreur lors de la décomposition : {e}")
