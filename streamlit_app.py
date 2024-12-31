import os
import streamlit as st
from decouple import config  # Per gestire ambienti diversi

# Configurazione dell'ambiente
ENV = config("ENV", default="staging")
DEBUG = config("DEBUG", cast=bool, default=True)

# Configurazione Streamlit
st.set_page_config(page_title="Universal Mapper", layout="wide")

# Importa i moduli richiesti
from utils.auth import login, register, request_password_reset, reset_password
from utils.file_processing import upload_file, preview_file, get_columns, generate_output
from utils.profiles import load_profile, save_profile, list_profiles, delete_profile

# Mostra un avviso se siamo in modalità staging
if DEBUG:
    st.warning("⚠️ Sei in modalità STAGING!")

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

# Sidebar con logica condizionale
with st.sidebar:
    if not st.session_state["authenticated"]:
        # Sidebar visibile solo quando non autenticato
        st.subheader("Altre opzioni")
        if st.button("Vai alla Registrazione", key="goto_register_button_sidebar"):
            st.session_state["page"] = "register"

        if st.button("Hai dimenticato la password?", key="forgot_password_button_sidebar"):
            st.session_state["page"] = "Reset Password"
    else:
        # Sidebar visibile quando autenticato
        st.title("Navigazione")
        page = st.radio(
            "Vai a:",
            options=["Caricamento File", "Gestione Profili", "Account", "Manuale", "Logout"],
            key="page_selector"
        )
        st.session_state["page"] = page

# Pagina di Login
if st.session_state["page"] == "login":
    st.title("Login")

    # Campi di input per username e password
    username = st.text_input("Username", placeholder="Inserisci il tuo username", key="login_username")
    password = st.text_input("Password", placeholder="Inserisci la tua password", type="password", key="login_password")

    # Bottone per il login
    login_clicked = st.button("Login", key="login_button")

    if login_clicked:
        if username and password:
            if login(username, password):  # Chiama la funzione di autenticazione
                st.success("Login riuscito! Reindirizzamento in corso...")
                st.session_state["authenticated"] = True
                st.session_state["page"] = "Caricamento File"  # Passa alla pagina successiva
            else:
                st.error("Credenziali errate. Riprova.")
        else:
            st.error("Entrambi i campi sono obbligatori.")

# Pagina di Registrazione
elif st.session_state["page"] == "register":
    st.title("Registrazione")
    new_username = st.text_input("Nuovo Username", key="register_username")
    new_password = st.text_input("Nuova Password", type="password", key="register_password")
    if st.button("Registrati", key="register_button"):
        if new_username and new_password:
            if register(new_username, new_password):
                st.success("Registrazione completata! Procedi con il login.")
                st.session_state["page"] = "login"
            else:
                st.error("L'utente esiste già.")
        else:
            st.error("Compila tutti i campi.")
    if st.button("Torna al Login", key="back_to_login_button"):
        st.session_state["page"] = "login"

# Pagina di Reset Password
elif st.session_state["page"] == "Reset Password":
    st.title("Reset Password")
    username = st.text_input("Inserisci il tuo username per inviare un'email di reset:", key="reset_username")
    if st.button("Invia Email", key="send_reset_email_button"):
        if request_password_reset(username):
            st.success("Email inviata! Controlla la tua casella di posta.")
        else:
            st.error("Utente non trovato.")
    token = st.text_input("Inserisci il token ricevuto via email:", key="reset_token")
    new_password = st.text_input("Inserisci la nuova password:", type="password", key="new_password")
    if st.button("Reimposta Password", key="reset_password_button"):
        if reset_password(token, new_password):
            st.success("Password aggiornata con successo!")
            st.session_state["page"] = "login"
        else:
            st.error("Token non valido o scaduto.")
    if st.button("Torna al Login", key="back_to_login_from_reset_button"):
        st.session_state["page"] = "login"

# Pagina di Caricamento File
elif st.session_state["page"] == "Caricamento File":
    st.title("Caricamento File")
    st.write("Carica i file sorgente e il tracciato record. Se hai un profilo salvato, puoi caricarlo per autocompilare le associazioni.")
    uploaded_source = upload_file("Carica file sorgente (CSV/XLS/XLSX):")
    uploaded_record = upload_file("Carica file tracciato record (CSV/XLS/XLSX):")
    # Logica aggiuntiva...

# Altre pagine come Gestione Profili, Account, Manuale, Logout...
elif st.session_state["page"] == "Gestione Profili":
    st.title("Gestione Profili")
    # Logica per gestire i profili salvati...
elif st.session_state["page"] == "Account":
    st.title("Impostazioni Account")
    # Logica per gestire l'account...
elif st.session_state["page"] == "Manuale":
    st.title("Manuale Utente")
    # Mostra il manuale...
elif st.session_state["page"] == "Logout":
    st.session_state["authenticated"] = False
    st.session_state["page"] = "login"
    st.success("Disconnesso con successo!")
