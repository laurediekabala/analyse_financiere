import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.data_loader import load_unemployment_data
from utils.model_loader import load_lstm_model, load_scaler,predict_lstm_future,predict_lstm_future_confidence,plot_lstm_predictions
from io import BytesIO
import os

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Veuillez vous connecter pour accéder à cette page.")
    st.stop()

st.set_page_config(
    page_title="Prédiction LSTM",
    page_icon="🔮",
    layout="wide"
)

st.title("🔮 Prédiction du Taux de Chômage aux USA avec LSTM")
st.markdown("Utilisez notre modèle LSTM pour prédire les futurs taux de chômage et visualiser les tendances à venir.")

df = load_unemployment_data()['unemploy']
# Charger le modèle LSTM (ou le créer si non existant)
model = load_lstm_model()
scaler= load_scaler()
st.subheader("Paramètres de Prédiction")
    
col1, col2 = st.columns([1,1])
with col1:
        n_future_steps = st.slider(
            "Nombre de mois à prédire dans le futur", 
            min_value=1, 
            max_value=36, 
            value=12
        )
with col2:
        confidence_level = st.slider(
            "Niveau de confiance pour l'intervalle (%)",
            min_value=1.645,
            max_value=1.96,
            value=2.576
        ) 

if st.button("Lancer la Prédiction", help="Cliquez pour générer les prédictions et le graphique"):
        st.subheader(f"Prédictions pour les {n_future_steps} prochains mois")

        # Obtenir les prédictions avec intervalle de confiance
        pred=predict_lstm_future(model,scaler,df,n_future_steps,30)
        st.dataframe(pred)
    
        csv_buffer = BytesIO()
        pred.to_csv(csv_buffer, index=True)
        st.download_button(
                label="Télécharger les prédictions (CSV)",
                data=csv_buffer.getvalue(),
                file_name="unemployment_predictions.csv",
                mime="text/csv",
                help="Cliquez pour télécharger le DataFrame des prédictions."
            )
if st.button("Lancer la Prédiction avec interval de confiance", help="Cliquez pour générer les prédictions avec intervall de confiance"):
        st.subheader(f"Prédictions pour les {n_future_steps} prochains mois")

        # Obtenir les prédictions avec intervalle de confiance
        preds=predict_lstm_future_confidence(model,scaler,df,n_future_steps,30,confidence_level)
        st.dataframe(preds)
    
        csv_buffer = BytesIO()
        preds.to_csv(csv_buffer, index=True)
        st.download_button(
                label="Télécharger les prédictions (CSV)",
                data=csv_buffer.getvalue(),
                file_name="unemployment_predictions.csv",
                mime="text/csv",
                help="Cliquez pour télécharger le DataFrame des prédictions."
            )        

st.subheader("Graphique des Prédictions avec Intervalle de Confiance")
pred=predict_lstm_future(model,scaler,df,n_future_steps,30)
preds=predict_lstm_future_confidence(model,scaler,df,n_future_steps,30,confidence_level)
plot_lstm_predictions(df,pred,preds)

st.markdown("""
<div style='text-align: justify; margin-top: 2em; font-size: 1.1em;'>
    Le modèle LSTM (Long Short-Term Memory) est un type de réseau de neurones récurrents (RNN) particulièrement adapté
    pour analyser et prédire des séquences temporelles. Il est capable de "se souvenir" d'informations sur de longues périodes,
    ce qui le rend efficace pour capter les dépendances complexes dans les séries chronologiques comme le taux de chômage.
    L'intervalle de confiance vous donne une plage probable dans laquelle la valeur réelle pourrait se situer,
    reflétant l'incertitude inhérente à toute prédiction.
</div>
""", unsafe_allow_html=True)