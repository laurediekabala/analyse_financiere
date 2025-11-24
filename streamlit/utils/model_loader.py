import numpy as np
import pandas as pd
import streamlit as st
from tensorflow.keras.models import load_model
import joblib
import os

# --- Chargement du modèle ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@st.cache_resource
def load_lstm_model():
    try:
        model_path = os.path.join(BASE_DIR, "..", "models", "lstm_univariate.h5")
        model_path = os.path.abspath(model_path)
        if not os.path.isfile(model_path):
            st.error(f"⚠️ Le modèle '{model_path}' est introuvable !")
            return None
        return load_model(model_path)
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement du modèle : {e}")
        return None
# --- Chargement du scaler ---
@st.cache_resource
def load_scaler():
    try:
        scaler_path = os.path.join(BASE_DIR, "..", "models", "scaler.pkl")
        scaler_path = os.path.abspath(scaler_path)
        if not os.path.isfile(scaler_path):
            st.error(f"⚠️ Le scaler '{scaler_path}' est introuvable !")
            return None
        return joblib.load(scaler_path)
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement du scaler : {e}")
        return None

# --- Fonction de prédiction ---
def predict_lstm_future(model, scaler, df, future_months=12, sequence_length=30):
    """
    Prédit les valeurs futures avec LSTM et retourne un DataFrame avec les dates.
    Compatible numpy.ndarray ou pandas.DataFrame.
    Les dates futures commencent au premier jour du mois suivant la dernière date du DataFrame.
    """
    # Convertir en DataFrame si c'est un ndarray
    if isinstance(df, np.ndarray):
        df = pd.DataFrame(df)

    # Vérification des données
    if model is None or scaler is None or len(df) == 0 or len(df) < sequence_length:
        st.warning("Les données sont insuffisantes ou le modèle n'est pas chargé.")
        return pd.DataFrame()

    data = df.copy()
    predictions = []
    data=df.values.reshape(-1, 1)

    # --- Création des dates futures basées sur la dernière date connue ---
    last_date = df.index[-1]
    dates_future = pd.date_range(start=last_date + pd.offsets.MonthBegin(1),
                                 periods=future_months, freq='MS')

    # Séquence initiale pour LSTM
    sequence = data[-sequence_length:]

    for _ in range(future_months):
        seq_scaled = scaler.transform(sequence)
        seq_scaled = seq_scaled.reshape((1, sequence_length, 1))
        pred_scaled = model.predict(seq_scaled, verbose=0)
        pred = scaler.inverse_transform(pred_scaled)[0, 0]
        predictions.append(pred)
        # Glissement de la séquence
        sequence = np.vstack([sequence[1:], [[pred]]])

    df_pred = pd.DataFrame({'date': dates_future, 'prediction': predictions})
    df_pred.set_index('date', inplace=True)
    return df_pred


def predict_lstm_future_confidence(model, scaler, df, future_months=12, sequence_length=30, z_score=1.96):
    """
    Prédit les valeurs futures avec LSTM et ajoute les intervalles de confiance.
    Compatible numpy.ndarray ou pandas.DataFrame.
    Les dates futures commencent au premier jour du mois suivant la dernière date du DataFrame.
    """
    if isinstance(df, np.ndarray):
        df = pd.DataFrame(df)

    if model is None or scaler is None or len(df) == 0 or len(df) < sequence_length:
        st.warning("Les données sont insuffisantes ou le modèle n'est pas chargé.")
        return pd.DataFrame()

    data = df.copy()
    data=df.values.reshape(-1, 1)
    predictions = []

    last_date = pd.to_datetime(df.index[-1])
    dates_future = pd.date_range(start=last_date + pd.offsets.MonthBegin(1),
                                 periods=future_months, freq='MS')

    sequence = data[-sequence_length:]

    for _ in range(future_months):
        seq_scaled = scaler.transform(sequence)
        seq_scaled = seq_scaled.reshape((1, sequence_length, 1))
        pred_scaled = model.predict(seq_scaled, verbose=0)
        pred = scaler.inverse_transform(pred_scaled)[0, 0]
        predictions.append(pred)
        sequence = np.vstack([sequence[1:], [[pred]]])

    df_conf = pd.DataFrame({'date': dates_future, 'prediction': predictions})
    df_conf.set_index('date', inplace=True)

    # Calcul des intervalles de confiance
    rolling_std = df_conf['prediction'].rolling(window=5, min_periods=1).std()
    df_conf['lower_bound'] = df_conf['prediction'] - z_score * rolling_std
    df_conf['upper_bound'] = df_conf['prediction'] + z_score * rolling_std

    return df_conf
import plotly.graph_objects as go
import streamlit as st

def plot_lstm_predictions(df_historical, df_pred, df_conf=None):
    """
    Trace les prédictions LSTM par rapport aux données historiques.
    
    Args:
        df_historical: DataFrame historique avec index datetime et colonne 'value'.
        df_pred: DataFrame avec les prédictions futures (index datetime, colonne 'prediction').
        df_conf: Optionnel. DataFrame avec 'lower_bound' et 'upper_bound' pour les intervalles de confiance.
    """
    fig = go.Figure()

    # Données historiques
    fig.add_trace(go.Scatter(
        x=df_historical.index,
        y=df_historical,  # suppose une seule colonne
        mode='lines+markers',
        name='Historique',
        line=dict(color='blue')
    ))

    # Prédictions
    fig.add_trace(go.Scatter(
        x=df_pred.index,
        y=df_pred['prediction'],
        mode='lines+markers',
        name='Prédiction LSTM',
        line=dict(color='orange', dash='dash')
    ))

    # Intervalle de confiance
    if df_conf is not None:
        fig.add_trace(go.Scatter(
            x=df_conf.index,
            y=df_conf['upper_bound'],
            mode='lines',
            name='Intervalle supérieur',
            line=dict(color='red'),
            showlegend=False
        ))
        fig.add_trace(go.Scatter(
            x=df_conf.index,
            y=df_conf['lower_bound'],
            mode='lines',
            name='Intervalle inférieur',
            line=dict(color='lightgrey'),
            fill='tonexty',
            fillcolor='rgba(200,200,200,0.3)',
            showlegend=True
        ))

    fig.update_layout(
        title="Prédictions LSTM vs Historique",
        xaxis_title="Date",
        yaxis_title="Valeur",
        template="plotly_white",
        legend=dict(x=0.01, y=0.99)
    )

    st.plotly_chart(fig, use_container_width=True)

