import streamlit as st
from utils.auth import authenticate_user, create_user, init_admin_user
import os

# Créer le dossier data s'il n'existe pas
if not os.path.exists('data'):
    os.makedirs('data')
# Initialiser l'utilisateur admin si ce n'est pas déjà fait
init_admin_user()

st.set_page_config(
    page_title="App Chômage USA",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Design professionnel ---
st.markdown("""
<style>
    .reportview-container .main .block-container{
        padding-top: 2rem;
        padding-right: 2rem;
        padding-left: 2rem;
        padding-bottom: 2rem;
    }
    .main {
        background-color: #f0f2f6; /* Light grey background */
    }
    .st-emotion-cache-z5rdhr { /* Sidebar background */
        background-color: #ffffff; 
    }
    .st-emotion-cache-z5rdhr h1, .st-emotion-cache-z5rdhr h2, .st-emotion-cache-z5rdhr h3 {
        color: #004d40; /* Dark teal for headings in sidebar */
    }
    .stButton>button {
        background-color: #00796b; /* Teal button */
        color: white;
        border-radius: 5px;
        padding: 0.6em 1.2em;
        font-size: 1.1em;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #004d40; /* Darker teal on hover */
        border-color: #004d40;
    }
    .css-1d391kg { /* Expander for login */
        background-color: #e0f2f1; /* Light teal for expander */
        border-left: 5px solid #00796b;
        padding: 10px;
        border-radius: 5px;
    }
    .css-1d391kg p {
        color: #004d40;
    }
    /* Style for the main welcome message */
    .welcome-header {
        font-size: 3em;
        color: #004d40;
        text-align: center;
        margin-bottom: 0.5em;
        font-weight: bold;
    }
    .welcome-subheader {
        font-size: 1.5em;
        color: #333;
        text-align: center;
        margin-bottom: 1.5em;
    }
    .center-button {
        display: flex;
        justify-content: center;
        margin-top: 2em;
    }
</style>
""", unsafe_allow_html=True)


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("Bienvenue sur notre application dédiée  à la prediction au nombre de chômageurs aux USA")
    st.subheader("Veuillez vous connecter pour accéder au contenu.")
    col1, col2 = st.columns([1, 1])

    with col1:
        with st.expander("Connexion", expanded=True):
            st.markdown("### Se connecter")
            username = st.text_input("Nom d'utilisateur")
            password = st.text_input("Mot de passe", type="password")

            if st.button("Se connecter"):
                if authenticate_user(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success("Connexion réussie !")
                    st.rerun() # Recharger l'application pour afficher les pages
                else:
                    st.error("Nom d'utilisateur ou mot de passe incorrect.")

    with col2:
        with st.expander("Créer un compte", expanded=False):
            st.markdown("### S'inscrire")
            new_username = st.text_input("Nouveau nom d'utilisateur")
            new_password = st.text_input("Nouveau mot de passe", type="password")
            confirm_password = st.text_input("Confirmer le mot de passe", type="password")

            if st.button("S'inscrire"):
                if new_username and new_password and confirm_password:
                    if new_password == confirm_password:
                        if create_user(new_username, new_password):
                            st.success("Compte créé avec succès ! Vous pouvez maintenant vous connecter.")
                        else:
                            st.error("Ce nom d'utilisateur existe déjà.")
                    else:
                        st.error("Les mots de passe ne correspondent pas.")
                else:
                    st.error("Veuillez remplir tous les champs.")

else:
    # La logique pour les pages est gérée par Streamlit, les fichiers dans 'pages/' seront détectés
    st.sidebar.title(f"Bienvenue, {st.session_state.username} !")
    if st.sidebar.button("Déconnexion"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.rerun()
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Navigation")
    # Streamlit gère la navigation des pages en fonction des fichiers dans 'pages/'
    st.info("Veuillez utiliser la barre latérale pour naviguer.")