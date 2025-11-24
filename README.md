# Prévision du Taux de Chômage aux États-Unis 🇺🇸

## Aperçu du Projet

Ce projet propose une approche avancée pour prédire le nbr des chômeurs aux États-Unis sur la période **1967-2015**, en utilisant à la fois des modèles statistiques classiques et des réseaux de neurones profonds (LSTM). L'objectif est de fournir des prévisions fiables basées sur les indicateurs économiques historiques.

---

## Modèles Testés

- **ARIMA / SARIMA / SARIMAX** : performances insuffisantes pour capturer les variations temporelles.  
- **Prophet** : incapable de modéliser efficacement la dynamique du chômage.  
- **LSTM (Réseau de neurones récurrent)** : capture efficacement les dépendances temporelles et fournit les meilleures performances.

---

## Résultats du Modèle LSTM

| Jeu de données | EMAE | R²    |
|----------------|------|-------|
| Entraînement   | 0.066 | 97%   |
| Test           | 0.17  | 95%   |

Ces résultats démontrent la capacité du LSTM à prédire avec précision le taux de chômage, surpassant les modèles classiques.

---

## Visualisation

![Exemple de prédiction LSTM](path_to_graphic.png)

*Graphique illustrant les prédictions du modèle LSTM et les intervalles de confiance.*

---

## Structure du Projet

- `streamlit/` : Application interactive pour visualiser les prédictions.  
- `models/` : Modèle LSTM pré-entraîné et scaler.  
- `utils/` : Fonctions utilitaires pour chargement de données et modèles.  
- `notebooks/` : Analyses exploratoires et expérimentations.  
- `data/` : Jeux de données bruts et prétraités.

---

## Lancement de l’Application

1. Installer les dépendances :

```bash
pip install -r requirements.txt
