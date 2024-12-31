import hashlib

# Nome file del database utenti
AUTH_FILE = "utils/auth.py"

def add_user(username, email, password):
    """Aggiungi un utente manualmente al database."""
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    new_user_entry = f'"{username}": {{"email": "{email}", "password": "{hashed_password}"}},\n'
    
    # Modifica il file auth.py
    with open(AUTH_FILE, "r") as f:
        lines = f.readlines()
    
    # Trova il punto in cui aggiungere il nuovo utente
    for i, line in enumerate(lines):
        if "USERS = {" in line:
            lines.insert(i + 1, f"    {new_user_entry}")
            break
    
    with open(AUTH_FILE, "w") as f:
        f.writelines(lines)

    print(f"Utente {username} aggiunto con successo!")

# Esempio di utilizzo
add_user("revan", "sviluppo@revan.it", "Frabicom,2010")
add_user("nilufar", "it@nilufar.com", "Nilve@2024_25")

