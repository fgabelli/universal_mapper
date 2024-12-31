import hashlib
import random
import string
import smtplib
from email.mime.text import MIMEText

# Simulazione database utenti
USERS = {
    "nilufar": {"email": "it@nilufar.com", "password": "64b3e3b48906caa365d0d152f2008bb602064ddca9972d7e2d51dc2bba44a3d7"},
    "revan": {"email": "sviluppo@revan.it", "password": "ca51e6e7d4662a728a6d14797fd568354fadc233021455998816f821d3aeb7ae"},
    "cliente3": {"email": "cliente3@example.com", "password": "d29550f242699b2504283a52ecbdff7e5945b7f01c92203e3a241e45b53b76bb"},
    "user1": {"email": "user1@example.com", "password": hashlib.sha256("password1".encode()).hexdigest()},
    "user2": {"email": "user2@example.com", "password": hashlib.sha256("password2".encode()).hexdigest()},
}

# Simulazione di token per reset password
RESET_TOKENS = {}

# Configurazione email (da personalizzare)
EMAIL_ADDRESS = "youremail@example.com"
EMAIL_PASSWORD = "yourpassword"
SMTP_SERVER = "smtp.example.com"
SMTP_PORT = 587

def login(username, password):
    """Verifica le credenziali di accesso."""
    if username in USERS:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if USERS[username]["password"] == hashed_password:
            return True
    return False

def register(username, password):
    """Registra un nuovo utente."""
    if username not in USERS:
        USERS[username] = {
            "email": f"{username}@example.com",  # Usa un'email fittizia
            "password": hashlib.sha256(password.encode()).hexdigest(),
        }
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
        send_reset_email(email, token)
        return True
    return False

def reset_password(token, new_password):
    """Resetta la password utilizzando il token."""
    if token in RESET_TOKENS:
        username = RESET_TOKENS.pop(token)
        USERS[username]["password"] = hashlib.sha256(new_password.encode()).hexdigest()
        return True
    return False
