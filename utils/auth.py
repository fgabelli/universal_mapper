import os
import json
import hashlib
import random
import string
import smtplib
from email.mime.text import MIMEText
from config import EMAIL_ADDRESS, EMAIL_PASSWORD, SMTP_SERVER, SMTP_PORT

USERS_FILE = os.path.join(os.path.dirname(__file__), "users.json")

# Carica gli utenti dal file
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

# Salva gli utenti nel file
def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

# Inizializza gli utenti
USERS = load_users()

RESET_TOKENS = {}

def login(username, password):
    if username in USERS:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if USERS[username]["password"] == hashed_password:
            return True
    return False

def register(username, password):
    if username not in USERS:
        USERS[username] = {
            "email": f"{username}@example.com",  # Genera un'email fittizia per questo esempio
            "password": hashlib.sha256(password.encode()).hexdigest(),
        }
        save_users(USERS)
        return True
    return False

def generate_token():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=32))

def send_reset_email(email, token):
    reset_link = f"http://localhost:8501/reset_password?token={token}"
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
        save_users(USERS)
        return True
    return False
