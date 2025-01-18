import hashlib
from utils.database import get_connection

# Funzione per generare l'hash della password
def hash_password(password):
    """Genera un hash SHA-256 per la password."""
    return hashlib.sha256(password.encode()).hexdigest()

# Funzione per registrare un utente
def register(email, password):
    hashed_password = hash_password(password)
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (email, password) VALUES (%s, %s)",
                (email, hashed_password)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Errore durante la registrazione: {e}")
            return False

# Funzione per autenticare un utente
def login(email, password):
    hashed_password = hash_password(password)
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT * FROM users WHERE email = %s AND password = %s",
                (email, hashed_password)
            )
            user = cursor.fetchone()
            return user is not None
        except Exception as e:
            print(f"Errore durante il login: {e}")
            return False

# Funzione di debug per verificare gli utenti nel database
def debug_check_users():
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, email, created_at FROM users")
            return cursor.fetchall()
        except Exception as e:
            print(f"Errore durante il debug degli utenti: {e}")
            return []
