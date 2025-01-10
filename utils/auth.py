import hashlib
import random
import string
import smtplib
import os
from email.mime.text import MIMEText

# Configurazione email (da personalizzare)
EMAIL_ADDRESS = "youremail@example.com"
EMAIL_PASSWORD = "yourpassword"
SMTP_SERVER = "smtp.example.com"
SMTP_PORT = 587

# Credenziali temporanee
USERS = {
    "admin": {
        "email": "admin@example.com",
        "password": hashlib.sha256("password".encode()).hexdigest()  # password: "password"
    },
    "testuser": {
        "nilufar": "it@nilufar.com",
        "password": hashlib.sha256("Nilve@2024_25".encode()).hexdigest()  # password: "Nilve@2024_25"
    }
}

# Funzioni di autenticazione
def login(username, password):
    """Verifica le credenziali di accesso."""
    print(f"DEBUG: Tentativo di login per {username}")  # Logga l'utente che tenta l'accesso
    print(f"DEBUG: USERS disponibili: {USERS}")  # Logga gli utenti caricati
    if username in USERS:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        print(f"DEBUG: Password inserita hashata: {hashed_password}")
        print(f"DEBUG: Password attesa: {USERS[username]['password']}")
        if USERS[username]["password"] == hashed_password:
            print("DEBUG: Login riuscito!")
            return True
        else:
            print("DEBUG: Password errata!")
    else:
        print("DEBUG: Nome utente non trovato!")
    return False

def register(username, password):
    """Registra un nuovo utente."""
    if username not in USERS:
        USERS[username] = {
            "email": f"{username}@example.com",  # Usa un'email fittizia
            "password": hashlib.sha256(password.encode()).hexdigest(),
        }
        print("DEBUG: Registrato nuovo utente.")
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
        print(f"DEBUG: Token generato per {username}: {token}")
        send_reset_email(email, token)
        return True
    return False

def reset_password(token, new_password):
    """Resetta la password utilizzando il token."""
    print(f"DEBUG: Token non gestito in memoria, la funzione è stata richiamata con il token {token}.")
    return False
