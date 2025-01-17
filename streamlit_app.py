import streamlit as st
from utils.database import initialize_db, register, login, debug_check_users
import pandas as pd
import os

# Configurazione Streamlit
st.set_page_config(page_title="Universal Mapper", layout="wide")

# Inizializza il database
initialize_db()

# Stato iniziale
if "page" not in st.session_state:
    st.session_state["page"] = "login"
if "authenticated_user" not in st.session_state:
    st.session_state["authenticated_user"] = None
if "uploaded_file" not in st.session_state:
    st.session_state["uploaded_file"] = None
if "mapping_profile" not in st.session_state:
    st.session_state["mapping_profile"] = {}

# Navigazione
def navigate_to(page):
    st.session_state["page"] = page

# Funzione per caricare un file
def upload_file():
    st.header("Caricamento File")
    uploaded_file = st.file_uploader("Carica il file sorgente (CSV, XLS, XLSX):")
    if uploaded_file:
        file_extension = os.path.splitext(uploaded_file.name)[1]
        if file_extension.lower() in [".csv", ".xls", ".xlsx"]:
            st.session_state["uploaded_file"] = uploaded_file
            st.success(f"File '{uploaded_file.name}' caricato con successo!")
        else:
            st.error("Formato file non supportato. Usa CSV, XLS o XLSX.")

# Funzione per associare colonne
def map_columns():
    st.header("Associazione Colonne")
    if not st.session_state["uploaded_file"]:
        st.error("Carica un file prima di procedere.")
        return

    st.write("Qui puoi associare le colonne del file sorgente al tracciato record.")
    columns = ["Colonna 1", "Colonna 2", "Colonna 3"]  # Esempio di colonne
    mappings = {}

    for col in columns:
        selected = st.selectbox(f"Associa per {col}", options=["Colonna A", "Colonna B", "Colonna C"], key=f"mapping_{col}")
        mappings[col] = selected

    st.session_state["mapping_profile"] = mappings
    st.success("Associazioni salvate.")

# Funzione per generare il file di output
def generate_output():
    st.header("Generazione File di Output")
    if not st.session_state["mapping_profile"]:
        st.error("Completa l'associazione delle colonne prima di procedere.")
        return

    st.write("Generazione in corso...")
    st.download_button("Scarica il file generato", data="Dati generati", file_name="output.csv")

# Pagina di Login
if st.session_state["page"] == "login":
    st.title("Login")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Accedi"):
        if login(email, password):
            st.success(f"Accesso effettuato! Benvenuto {email}.")
            st.session_state["authenticated_user"] = email
            navigate_to("dashboard")
        else:
            st.error("Email o password errati.")

# Pagina di Registrazione
elif st.session_state["page"] == "register":
    st.title("Registrazione")
    email = st.text_input("Email", key="register_email")
    password = st.text_input("Password", type="password", key="register_password")
    if st.button("Registrati"):
        if register(email, password):
            st.success("Registrazione completata! Torna al login per accedere.")
            navigate_to("login")
        else:
            st.error("Errore nella registrazione: l'utente potrebbe già esistere.")

# Dashboard
elif st.session_state["page"] == "dashboard":
    st.title("Dashboard")
    st.write(f"Benvenuto, {st.session_state['authenticated_user']}!")
    st.write("Seleziona un'opzione dalla barra laterale.")

# Sidebar
with st.sidebar:
    st.title("Navigazione")
    if st.session_state["page"] == "login":
        if st.button("Registrati"):
            navigate_to("register")
    elif st.session_state["page"] == "dashboard":
        if st.button("Caricamento File"):
            navigate_to("upload_file")
        if st.button("Associazione Colonne"):
            navigate_to("map_columns")
        if st.button("Generazione Output"):
            navigate_to("generate_output")
        if st.button("Esci"):
            st.session_state["authenticated_user"] = None
            navigate_to("login")

# Pagine dinamiche
if st.session_state["page"] == "upload_file":
    upload_file()
elif st.session_state["page"] == "map_columns":
    map_columns()
elif st.session_state["page"] == "generate_output":
    generate_output()
