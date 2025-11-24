import streamlit as st

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Veuillez vous connecter pour accéder à cette page.")
    st.stop()

st.set_page_config(
    page_title="À propos",
    page_icon="ℹ️",
    layout="wide"
)

st.title("ℹ️ À Propos de l'Application")

st.markdown("""
<div style='text-align: justify; margin-top: 1em; font-size: 1.1em;'>
    Cette application a été développée pour offrir une plateforme interactive et professionnelle d'analyse et de prédiction
    du taux de chômage aux États-Unis. Elle s'adresse aux analystes de données, économistes, chercheurs,
    et à toute personne intéressée par les dynamiques du marché du travail américain.
</div>
""", unsafe_allow_html=True)

st.subheader("Importance de l'Application")
st.markdown("""
<div style='text-align: justify; font-size: 1.1em;'>
L'accès rapide et la visualisation claire des données de chômage sont cruciaux pour plusieurs raisons :

* **Prise de Décision Économique :** Les décideurs politiques et les économistes utilisent ces données pour évaluer la santé de l'économie,
    formuler des politiques monétaires et budgétaires, et anticiper les récessions ou les périodes de croissance.
* **Stratégie d'Entreprise :** Les entreprises peuvent adapter leurs stratégies d'embauche, d'investissement et de production
    en fonction des prévisions du marché du travail.
* **Recherche et Analyse :** Les chercheurs peuvent explorer les corrélations avec d'autres indicateurs économiques
    et développer des modèles prédictifs plus sophistiqués.
* **Information Publique :** Offrir une compréhension transparente et accessible des tendances du chômage au grand public.

En fournissant des outils d'analyse descriptive et des capacités de prédiction basées sur des modèles de pointe comme le LSTM,
cette application vise à démocratiser l'accès à l'intelligence économique et à soutenir une meilleure compréhension des marchés.
</div>
""", unsafe_allow_html=True)

st.subheader("Contact")
st.markdown("""
Pour toute question, suggestion ou collaboration, n'hésitez pas à me contacter :
* **Email :** [laurediekabala@gmail.com](mailto:laurediekabala@gmail.com)
""")

st.markdown("""
<br><br>
<div style='text-align: center; font-size: 0.9em; color: gray;'>
    © 2023 Application de Prédiction du Chômage. Tous droits réservés.
</div>
""", unsafe_allow_html=True)