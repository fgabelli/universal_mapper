import psycopg2
from psycopg2.extras import RealDictCursor
import hashlib
import os

# Ottieni la stringa di connessione dal database
DB_URL = os.getenv("DB_URL")

# Connessione al database
def get_connection():
    return psycopg2.connect(DB_URL, cursor_factory=RealDictCursor)

# Creazione delle tabelle
# Nota: Su Supabase, le tabelle dovrebbero essere gestite tramite il dashboard o script separati.

# Funzione per registrare un utente
def register(email, password):
    hashed_password = hash_password(password)
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO users (email, password) VALUES (%s, %s)",
                    (email, hashed_password)
                )
                conn.commit()
                print(f"Utente registrato: {email}")  # Debug
                return True
    except psycopg2.IntegrityError as e:
        print(f"Errore durante la registrazione: {e}")  # Debug
        return False  # L'email è già registrata
    except Exception as e:
        print(f"Errore generale durante la registrazione: {e}")
        return False

# Funzione per autenticare un utente
def login(email, password):
    hashed_password = hash_password(password)
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
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
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
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
