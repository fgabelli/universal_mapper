import sqlite3
import hashlib
import os

# Ottieni il percorso del database SQLite
DB_PATH = os.getenv("DB_PATH", "database.db")  # Usa un file di default chiamato 'database.db'

# Connessione al database
def get_connection():
    """Crea una connessione al database SQLite."""
    return sqlite3.connect(DB_PATH)

# Funzione per registrare un utente
def register(email, password):
    """Registra un nuovo utente nel database."""
    hashed_password = hash_password(password)
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (email, password) VALUES (?, ?)",
                (email, hashed_password)
            )
            conn.commit()
            print(f"Utente registrato: {email}")  # Debug
            return True
    except sqlite3.IntegrityError:
        print(f"Errore: L'email '{email}' è già registrata.")  # Debug
        return False
    except Exception as e:
        print(f"Errore generale durante la registrazione: {e}")
        return False

# Funzione per autenticare un utente
def login(email, password):
    """Autentica un utente esistente."""
    hashed_password = hash_password(password)
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE email = ? AND password = ?",
                (email, hashed_password)
            )
            user = cursor.fetchone()
            return user is not None
    except Exception as e:
        print(f"Errore durante il login: {e}")
        return False

# Funzione di debug per verificare gli utenti nel database
def debug_check_users():
    """Restituisce un elenco di tutti gli utenti nel database (solo per debug)."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, email, created_at FROM users")
            users = cursor.fetchall()
            return users
    except Exception as e:
        print(f"Errore durante il debug degli utenti: {e}")
        return []

# Funzione per generare l'hash della password
def hash_password(password):
    """Genera un hash SHA-256 per la password."""
    return hashlib.sha256(password.encode()).hexdigest()
