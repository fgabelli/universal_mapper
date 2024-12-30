import json
import os

# Percorso del file utenti
USERS_FILE = "users.json"

# Funzione per inizializzare il file utenti
def initialize_users_file():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as file:
            json.dump({}, file)

# Funzione per registrare un nuovo utente
def register(username, password):
    initialize_users_file()
    with open(USERS_FILE, "r") as file:
        users = json.load(file)
    
    if username in users:
        return False  # Username già esistente
    
    users[username] = {"password": password}
    with open(USERS_FILE, "w") as file:
        json.dump(users, file)
    return True

# Funzione per effettuare il login
def login(username, password):
    initialize_users_file()
    with open(USERS_FILE, "r") as file:
        users = json.load(file)
    
    if username in users and users[username]["password"] == password:
        return True
    return False
