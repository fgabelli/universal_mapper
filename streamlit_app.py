import os
import json
import streamlit as st
from decouple import config
from utils.auth import login, register, request_password_reset, reset_password
from utils.file_processing import upload_file, preview_file, get_columns, generate_output
from utils.profiles import load_profile, save_profile, list_profiles, delete_profile

# Configurazione dell'app - deve essere il PRIMO comando Streamlit
st.set_page_config(page_title="Universal Mapper", layout="wide")

# Funzione per mostrare l'intestazione con logo e nome app
def show_header():
    col1, col2 = st.columns([1, 5])
    logo_path = os.path.join(os.path.dirname(__file__), "logo", "logo_web.png")
    try:
        with col1:
            st.image(logo_path, width=80)  # Carica il logo
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
    except Exception as e:
        st.error(f"Errore nel caricamento del logo: {e}")

# Mostra l'intestazione nella parte superiore di ogni pagina
show_header()

# Inizializza lo stato
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "page" not in st.session_state:
    st.session_state["page"] = "login"
if "associations" not in st.session_state:
    st.session_state["associations"] = []

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
        if st.button("Hai dimenticato la password?", key="forgot_password_button_sidebar"):
            st.session_state["page"] = "Reset Password"

# Funzione di gestione delle pagine
def handle_navigation(page_name):
    """Cambia la pagina attiva."""
    st.session_state["page"] = page_name

# Gestione delle pagine principali
if st.session_state["page"] == "login":
    st.title("Login")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login", key="login_button"):
        if login(email, password):
            st.session_state["authenticated"] = True
            handle_navigation("Caricamento File")
        else:
            st.error("Credenziali errate.")

elif st.session_state["page"] == "register":
    st.title("Registrazione")
    email = st.text_input("Email", key="register_email")
    password = st.text_input("Password", type="password", key="register_password")
    if st.button("Registrati", key="register_button"):
        if email and password:
            if register(email, password):
                st.success("Registrazione completata! Procedi con il login.")
                handle_navigation("login")
            else:
                st.error("L'utente esiste già.")
        else:
            st.error("Compila tutti i campi.")

elif st.session_state["page"] == "Caricamento File":
    st.title("Caricamento File")
    st.write("Carica i file sorgente e il tracciato record. Se hai un profilo salvato, puoi caricarlo per autocompilare le associazioni.")
    uploaded_source = upload_file("Carica file sorgente (CSV/XLS/XLSX):")
    uploaded_record = upload_file("Carica file tracciato record (CSV/XLS/XLSX):")

    if uploaded_source and uploaded_record:
        st.subheader("Anteprima file sorgente:")
        preview_file(uploaded_source)
        st.subheader("Anteprima file tracciato record:")
        preview_file(uploaded_record)

elif st.session_state["page"] == "Gestione Profili":
    st.title("Gestione Profili")
    profiles = list_profiles()
    if profiles:
        selected_profile = st.selectbox("Seleziona un profilo salvato", profiles)
        if st.button("Elimina Profilo"):
            delete_profile(selected_profile)
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

        #### **Funzionalità aggiuntive:**

        - **Reset Password**: Reimposta la password in caso di smarrimento.
        - **Impostazioni Account**: Modifica la password o gestisci i dettagli dell'account.

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
