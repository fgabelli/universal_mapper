import os
import json
import streamlit as st
from decouple import config
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import uuid

# Configurazione Streamlit
st.set_page_config(page_title="Universal Mapper", layout="wide")

# Percorsi dei file
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

# Inizializza lo stato
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "page" not in st.session_state:
    st.session_state["page"] = "login"

# Sidebar con logica condizionale
with st.sidebar:
    if not st.session_state["authenticated"]:
        st.subheader("Altre opzioni")
        if st.button("Vai alla Registrazione"):
            st.session_state["page"] = "register"
        if st.button("Hai dimenticato la password?"):
            st.session_state["page"] = "Reset Password"
    else:
        st.title("Navigazione")
        page = st.radio("Vai a:", options=["Caricamento File", "Gestione Profili", "Manuale", "Logout"], key="page_selector")
        st.session_state["page"] = page

# Pagine dell'applicazione
if st.session_state["page"] == "login":
    st.title("Login")
    email = st.text_input("Email", placeholder="Inserisci la tua email")
    password = st.text_input("Password", placeholder="Inserisci la tua password", type="password")

    if st.button("Login"):
        if email and password:
            if login(email, password):
                st.success("Login riuscito!")
                st.session_state["authenticated"] = True
                st.session_state["page"] = "Caricamento File"
            else:
                st.error("Email o password errati.")
        else:
            st.error("Entrambi i campi sono obbligatori.")

elif st.session_state["page"] == "register":
    st.title("Registrazione")
    email = st.text_input("Email", placeholder="Inserisci la tua email")
    password = st.text_input("Password", placeholder="Crea una password", type="password")

    if st.button("Registrati"):
        if email and password:
            if register(email, password):
                st.success("Registrazione completata! Procedi con il login.")
                st.session_state["page"] = "login"
            else:
                st.error("Email già registrata.")
        else:
            st.error("Compila tutti i campi.")

elif st.session_state["page"] == "Reset Password":
    st.title("Reset Password")
    email = st.text_input("Inserisci la tua email per ricevere un token di reset:")
    if st.button("Invia Email"):
        if request_password_reset(email):
            st.success("Email inviata! Controlla la tua casella di posta.")
        else:
            st.error("Email non trovata.")

    token = st.text_input("Inserisci il token ricevuto via email:")
    new_password = st.text_input("Inserisci la nuova password:", type="password")
    if st.button("Reimposta Password"):
        if reset_password(token, new_password):
            st.success("Password aggiornata con successo! Procedi con il login.")
            st.session_state["page"] = "login"
        else:
            st.error("Token non valido o scaduto.")

elif st.session_state["page"] == "Caricamento File":
    st.title("Caricamento File")
    uploaded_file = st.file_uploader("Carica un file CSV, XLS o XLSX", type=["csv", "xls", "xlsx"])
    if uploaded_file:
        st.success(f"File '{uploaded_file.name}' caricato con successo!")
    if st.button("Logout"):
        st.session_state["authenticated"] = False
        st.session_state["page"] = "login"
