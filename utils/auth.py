import hashlib
import random
import string
import smtplib
import json
import os
from email.mime.text import MIMEText

# Percorsi dei file di dati
USERS_FILE = os.path.join(os.path.dirname(__file__), "users.json")
RESET_TOKENS_FILE = os.path.join(os.path.dirname(__file__), "reset_tokens.json")

# Configurazione email (da personalizzare)
EMAIL_ADDRESS = "youremail@example.com"
EMAIL_PASSWORD = "yourpassword"
SMTP_SERVER = "smtp.example.com"
SMTP_PORT = 587

# Funzioni per gestire il caricamento e il salvataggio dei dati
def load_users():
    """Carica gli utenti dal file JSON."""
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    """Salva gli utenti nel file JSON."""
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

def load_reset_tokens():
    """Carica i token di reset dal file JSON."""
    if os.path.exists(RESET_TOKENS_FILE):
        with open(RESET_TOKENS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_reset_tokens(tokens):
    """Salva i token di reset nel file JSON."""
    with open(RESET_TOKENS_FILE, "w") as f:
        json.dump(tokens, f, indent=4)

# Carica dati iniziali
USERS = load_users()
RESET_TOKENS = load_reset_tokens()

# Funzioni di autenticazione
def login(username, password):
    """Verifica le credenziali di accesso con messaggi di debug."""
    print(f"DEBUG: Tentativo di accesso con username '{username}'")
    if username in USERS:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        print(f"DEBUG: Password hash inserita: {hashed_password}")
        print(f"DEBUG: Password hash attesa: {USERS[username]['password']}")
        if USERS[username]["password"] == hashed_password:
            print("DEBUG: Accesso riuscito!")
            return True
        else:
            print("DEBUG: Password errata.")
    else:
        print("DEBUG: Username non trovato.")
    return False

def register(username, password):
    """Registra un nuovo utente."""
    if username not in USERS:
        USERS[username] = {
            "email": f"{username}@example.com",  # Usa un'email fittizia
            "password": hashlib.sha256(password.encode()).hexdigest(),
        }
        save_users(USERS)
        return True
    return False

def generate_token():
    """Genera un token univoco per il reset della password."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=32))

def send_reset_email(email, token):
    """Invia un'email con il link per il reset della password."""
    reset_link = f"http://localhost:8501/reset_password?token={token}"  # Modifica con l'URL del tuo Streamlit Cloud
    message = MIMEText(f"Clicca qui per reimpostare la tua password: {reset_link}")
    message["Subject"] = "Reimposta la tua password"
    message["From"] = EMAIL_ADDRESS
    message["To"] = email

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(message)
    except Exception as e:
        print(f"Errore durante l'invio dell'email: {e}")

def request_password_reset(username):
    """Genera un token per il reset della password e invia un'email."""
    if username in USERS:
        email = USERS[username]["email"]
        token = generate_token()
        RESET_TOKENS[token] = username
        save_reset_tokens(RESET_TOKENS)
        send_reset_email(email, token)
        return True
    return False

def reset_password(token, new_password):
    """Resetta la password utilizzando il token."""
    if token in RESET_TOKENS:
        username = RESET_TOKENS.pop(token)
        USERS[username]["password"] = hashlib.sha256(new_password.encode()).hexdigest()
        save_users(USERS)
        save_reset_tokens(RESET_TOKENS)
        return True
    return False
