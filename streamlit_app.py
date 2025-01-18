import os
import json
import streamlit as st
import pandas as pd
from utils.database import initialize_db, get_connection
from utils.auth import login, register
from utils.file_processing import upload_file, preview_file, get_columns, generate_output
from utils.profiles import load_profile, save_profile, list_profiles, delete_profile

# Configurazione dell'app - deve essere il PRIMO comando Streamlit
st.set_page_config(page_title="Universal Mapper", layout="wide")

# Inizializza il database
initialize_db()

# Funzione per ottenere l'ID dell'utente basato sull'email
def get_user_id(email):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        return user[0] if user else None

# Funzione per mostrare l'intestazione con logo e nome app
def show_header():
    col1, col2 = st.columns([1, 5])
    logo_path = os.path.join(os.path.dirname(__file__), "logo", "logo_web.png")
    try:
        with col1:
            st.image(logo_path, width=80)
        with col2:
            st.markdown(
                """
                <div style="margin-top: -10px;">
                    <h1 style="margin-bottom: 0; font-size: 35px; font-family: Arial, sans-serif; color: #333;">
                        Universal Mapper
                    </h1>
                </div>
                """,
                unsafe_allow_html=True,
            )
    except Exception:
        st.error("Errore nel caricamento del logo")

# Mostra l'intestazione nella parte superiore di ogni pagina
show_header()

# Inizializza lo stato
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "authenticated_user" not in st.session_state:
    st.session_state["authenticated_user"] = None
if "page" not in st.session_state:
    st.session_state["page"] = "login"
if "associations" not in st.session_state:
    st.session_state["associations"] = []
if "output_file" not in st.session_state:
    st.session_state["output_file"] = None

# Sidebar per la navigazione
with st.sidebar:
    if st.session_state["authenticated"]:
        st.title("Navigazione")
        page = st.radio(
            "Vai a:",
            options=["Caricamento File", "Gestione Profili", "Account", "Manuale", "Logout"],
            key="page_selector"
        )
        st.session_state["page"] = page
    else:
        st.title("Accesso richiesto")
        if st.button("Vai alla Registrazione", key="goto_register_button_sidebar"):
            st.session_state["page"] = "register"

# Funzione di gestione delle pagine
def handle_navigation(page_name):
    st.session_state["page"] = page_name

# Gestione delle pagine principali
if st.session_state["page"] == "login":
    st.title("Login")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login", key="login_button"):
        if login(email, password):
            st.session_state["authenticated"] = True
            st.session_state["authenticated_user"] = email
            st.success("Accesso effettuato!")
            handle_navigation("Caricamento File")
        else:
            st.error("Email o password errati.")

elif st.session_state["page"] == "register":
    st.title("Registrazione")
    email = st.text_input("Email", key="register_email")
    password = st.text_input("Password", type="password", key="register_password")
    if st.button("Registrati", key="register_button"):
        if email and password:
            success = register(email, password)
            if success:
                st.success(f"Registrazione completata per: {email}")
            else:
                st.error("Registrazione fallita")
        else:
            st.error("Compila tutti i campi.")

elif st.session_state["page"] == "Caricamento File":
    st.title("Caricamento File")
    uploaded_source = upload_file("Carica file sorgente (CSV/XLS/XLSX):")
    uploaded_record = upload_file("Carica file tracciato record (CSV/XLS/XLSX):")

    if uploaded_source and uploaded_record:
        st.subheader("Anteprima file sorgente:")
        preview_file(uploaded_source)
        st.subheader("Anteprima file tracciato record:")
        preview_file(uploaded_record)

        profiles = list_profiles(st.session_state["authenticated_user"])
        if profiles:
            selected_profile = st.selectbox("Seleziona un profilo salvato", [p[1] for p in profiles])
            if st.button("Carica Profilo"):
                profile_data = load_profile(selected_profile)
                st.session_state["associations"] = profile_data

        source_columns = get_columns(uploaded_source)
        record_columns = get_columns(uploaded_record)
        associations = {}
        for record_col in record_columns:
            associations[record_col] = st.selectbox(
                f"Associa una colonna per '{record_col}':",
                options=["-- Nessuna --"] + source_columns,
                key=f"assoc_{record_col}",
            )
        st.session_state["associations"] = associations

        profile_name = st.text_input("Nome del profilo:")
        if st.button("Salva Profilo"):
            try:
                user_id = get_user_id(st.session_state["authenticated_user"])
                if user_id:
                    save_profile(user_id, profile_name, st.session_state["associations"])
                    st.success(f"Profilo '{profile_name}' salvato!")
                else:
                    st.error("Errore: Utente non trovato!")
            except Exception as e:
                st.error(f"Errore durante il salvataggio del profilo: {e}")

        output_format = st.selectbox("Seleziona il formato del file generato:", ["CSV", "XLS", "XLSX"])
        if st.button("Genera File"):
            try:
                output_file = generate_output(
                    uploaded_source, 
                    st.session_state["associations"], 
                    output_format
                )
                st.session_state["output_file"] = output_file
                st.success("File generato con successo!")
            except Exception as e:
                st.error(f"Errore durante la generazione del file: {e}")

        if st.session_state["output_file"]:
            with open(st.session_state["output_file"], "rb") as file:
                st.download_button(
                    label="Scarica il file generato",
                    data=file,
                    file_name=f"output.{output_format.lower()}",
                    mime="text/csv" if output_format == "CSV" else "application/vnd.ms-excel"
                )

elif st.session_state["page"] == "Gestione Profili":
    st.title("Gestione Profili")
    profiles = list_profiles(st.session_state["authenticated_user"])
    if profiles:
        selected_profile = st.selectbox("Seleziona un profilo salvato", [p[1] for p in profiles])
        if st.button("Elimina Profilo"):
            delete_profile(selected_profile, st.session_state["authenticated_user"])
            st.success(f"Profilo '{selected_profile}' eliminato!")
    else:
        st.warning("Non ci sono profili salvati.")

elif st.session_state["page"] == "Account":
    st.title("Impostazioni Account")
    new_password = st.text_input("Nuova Password", type="password")
    if st.button("Cambia Password"):
        reset_password(st.session_state["authenticated_user"], new_password)
        st.success("Password cambiata con successo!")

elif st.session_state["page"] == "Manuale":
    st.title("Manuale Utente")
    st.markdown(
        """
        ### Benvenuto nel Manuale Utente di Universal Mapper

        Questa applicazione ti consente di caricare file sorgente e tracciati record, associare colonne, generare file di output e gestire profili personalizzati.

        #### **Come utilizzare l'app:**

        1. **Login o Registrazione**:
           - Accedi utilizzando il tuo username e password.
           - Se non hai un account, utilizza il pulsante di registrazione per crearne uno.

        2. **Caricamento File**:
           - Carica il file sorgente (CSV, XLS, XLSX) e il tracciato record.
           - Visualizza un'anteprima dei file caricati per verificarne il contenuto.

        3. **Associazione Colonne**:
           - Associa le colonne del file sorgente a quelle del tracciato record.
           - Puoi caricare o salvare un profilo per semplificare il processo in futuro.

        4. **Generazione File di Output**:
           - Scegli il formato di output desiderato (CSV, XLS, XLSX).
           - Genera e scarica il file di output.

        5. **Gestione Profili**:
           - Visualizza ed elimina i profili salvati.

        #### **Supporto:**

        Per ulteriori informazioni o problemi tecnici, contatta il supporto tecnico.

        **Email:** supporto@revan.it  
        **Telefono:** +39 0245076239
        """
    )

elif st.session_state["page"] == "Logout":
    st.session_state["authenticated"] = False
    st.session_state["page"] = "login"
    st.success("Disconnesso con successo!")
