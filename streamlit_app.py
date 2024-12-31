import os
import json
import streamlit as st
from decouple import config

# Configurazione dell'app - deve essere il PRIMO comando Streamlit
st.set_page_config(page_title="Universal Mapper", layout="wide")

# Percorsi dei file JSON
USERS_FILE = os.path.join("utils", "users.json")
TOKENS_FILE = os.path.join("utils", "reset_tokens.json")

# Funzione per leggere un file JSON
def read_json(file_path):
    if not os.path.exists(file_path):
        return {}
    with open(file_path, "r") as file:
        return json.load(file)

# Funzione per scrivere un file JSON
def write_json(file_path, data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

# Funzioni per utenti
def read_users():
    return read_json(USERS_FILE)

def write_users(users):
    write_json(USERS_FILE, users)

# Funzioni per token
def read_tokens():
    return read_json(TOKENS_FILE)

def write_tokens(tokens):
    write_json(TOKENS_FILE, tokens)

# Funzione per inviare email
def send_email(to_email, subject, message):
    try:
        smtp_server = config("EMAIL_HOST", default="smtp.gmail.com")
        smtp_port = config("EMAIL_PORT", cast=int, default=587)
        smtp_user = config("EMAIL_USER")
        smtp_password = config("EMAIL_PASSWORD")

        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        msg = MIMEMultipart()
        msg["From"] = smtp_user
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, to_email, msg.as_string())
        return True
    except Exception as e:
        print(f"Errore nell'invio dell'email: {e}")
        return False

# Funzione per generare un token
def generate_token():
    import uuid
    return str(uuid.uuid4())

# Funzione per richiedere il reset della password
def request_password_reset(email):
    users = read_users()
    tokens = read_tokens()
    if email not in users:
        return False
    token = generate_token()
    tokens[email] = token
    write_tokens(tokens)
    message = f"Usa questo token per reimpostare la tua password: {token}"
    return send_email(email, "Reset della tua password", message)

# Funzione per reimpostare la password
def reset_password(token, new_password):
    users = read_users()
    tokens = read_tokens()
    for email, saved_token in tokens.items():
        if token == saved_token:
            users[email]["password"] = new_password
            write_users(users)
            del tokens[email]
            write_tokens(tokens)
            return True
    return False

# Funzione per il login
def login(email, password):
    users = read_users()
    return email in users and users[email]["password"] == password

# Funzione per la registrazione
def register(email, password):
    users = read_users()
    if email in users:
        return False
    users[email] = {"password": password}
    write_users(users)
    return True

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
            options=["Caricamento File", "Gestione Profili", "Account", "Manuale" , "Logout"],
            key="page_selector"
        )
        st.session_state["page"] = page
    else:
        st.title("Accesso richiesto")
        st.session_state["page"] = "login"

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
    if st.button("Vai alla Registrazione", key="goto_register_button"):
        handle_navigation("register")
    if st.button("Hai dimenticato la password?", key="forgot_password_button"):
        handle_navigation("Reset Password")

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
    if st.button("Torna al Login", key="back_to_login_button"):
        handle_navigation("login")

elif st.session_state["page"] == "Reset Password":
    st.title("Reset Password")
    email = st.text_input("Inserisci la tua email per inviare un'email di reset:", key="reset_email")
    if st.button("Invia Email", key="send_reset_email_button"):
        if request_password_reset(email):
            st.success("Email inviata! Controlla la tua casella di posta.")
        else:
            st.error("Utente non trovato.")
    token = st.text_input("Inserisci il token ricevuto via email:", key="reset_token")
    new_password = st.text_input("Inserisci la nuova password:", type="password", key="new_password")
    if st.button("Reimposta Password", key="reset_password_button"):
        if reset_password(token, new_password):
            st.success("Password aggiornata con successo!")
        else:
            st.error("Token non valido o scaduto.")
    if st.button("Torna al Login", key="back_to_login_from_reset_button"):
        handle_navigation("login")

elif st.session_state["page"] == "Caricamento File":
    st.title("Caricamento File")
    st.write("Carica i file sorgente e il tracciato record. Se hai un profilo salvato, puoi caricarlo per autocompilare le associazioni.")
    # Logica di caricamento file rimane invariata...

elif st.session_state["page"] == "Gestione Profili":
    st.title("Gestione Profili")
    # Logica di gestione profili rimane invariata...

elif st.session_state["page"] == "Account":
    st.title("Impostazioni Account")
    # Logica per gestione account rimane invariata...

elif st.session_state["page"] == "Manuale":
    st.title("Manuale Utente")
    # Manuale rimane invariato...

elif st.session_state["page"] == "Logout":
    st.session_state["authenticated"] = False
    st.session_state["page"] = "login"
    st.success("Disconnesso con successo!")
