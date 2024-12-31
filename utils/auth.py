# auth.py
import hashlib
import random
import string
import smtplib
from email.mime.text import MIMEText
from config import EMAIL_ADDRESS, EMAIL_PASSWORD, SMTP_SERVER, SMTP_PORT

# Simulazione database utenti
USERS = {
    "utente1": {"email": "utente1@example.com", "password": hashlib.sha256("password1".encode()).hexdigest()},
    "utente2": {"email": "utente2@example.com", "password": hashlib.sha256("password2".encode()).hexdigest()},
}

# Generazione di un token univoco
RESET_TOKENS = {}

def generate_token():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=32))

# Invio email
def send_reset_email(email, token):
    reset_link = f"http://localhost:8501/reset_password?token={token}"  # Cambia l'URL se necessario
    message = MIMEText(f"Clicca qui per reimpostare la tua password: {reset_link}")
    message["Subject"] = "Reimposta la tua password"
    message["From"] = EMAIL_ADDRESS
    message["To"] = email

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(message)

def request_password_reset(username):
    if username in USERS:
        email = USERS[username]["email"]
        token = generate_token()
        RESET_TOKENS[token] = username
        send_reset_email(email, token)
        return True
    return False

def reset_password(token, new_password):
    if token in RESET_TOKENS:
        username = RESET_TOKENS.pop(token)
        USERS[username]["password"] = hashlib.sha256(new_password.encode()).hexdigest()
        return True
    return False
