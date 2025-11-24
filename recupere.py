import wbdata
import pandas as pd
import datetime

# Indicateurs que tu veux récupérer : tu peux en ajouter d'autres
indicators = {
    "NY.GDP.MKTP.KD": "GDP_constant_USD",      # PIB constant (réel)
    "NY.GDP.MKTP.CD": "GDP_current_USD",       # PIB courant
    "FP.CPI.TOTL.ZG": "Inflation_annual_pct",  # Inflation, variation annuelle des prix à la consommation
    "NY.GDP.PCAP.KD": "GDP_per_capita_constant", # PIB par habitant constant
}

# Définir la période
data_dates = (datetime.datetime(1960, 1, 1), datetime.datetime(2023, 12, 31))

# Code pays pour la RDC
country_code = "COD"

# Télécharger les données
df = wbdata.get_dataframe(indicators, country=country_code, date=data_dates)

# Réinitialiser l’index pour avoir “date” comme colonne
df = df.reset_index()

# Afficher les premières lignes
print(df.head())

# Sauvegarder dans un CSV
df.to_csv("rdc_macro_1960_2023.csv", index=False)
print("CSV sauvegardé : rdc_macro_1960_2023.csv")
