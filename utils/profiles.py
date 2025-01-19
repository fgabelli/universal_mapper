import json
import sqlite3
import os

# Percorso del database SQLite
DB_PATH = os.getenv("DB_PATH", "universal_mapper.db")

def get_connection():
    """Ritorna una connessione al database SQLite."""
    return sqlite3.connect(DB_PATH)

# Funzione per ottenere l'ID dell'utente dato l'email
def get_user_id(email):
    """Restituisce l'ID dell'utente dato l'email."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
            user = cursor.fetchone()
            if not user:
                raise ValueError(f"Utente non trovato per email: {email}")
            return user[0]
    except Exception as e:
        raise ValueError(f"Errore durante il recupero dell'ID utente: {e}")

# Funzione per salvare un profilo
def save_profile(user_id, profile_name, associations):
    """Salva un profilo per l'utente specificato."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO profiles (user_id, name, data) VALUES (?, ?, ?)",
                (user_id, profile_name, json.dumps(associations)),
            )
            conn.commit()
    except Exception as e:
        raise ValueError(f"Errore durante il salvataggio del profilo: {e}")

# Funzione per recuperare tutti i profili di un utente
def list_profiles(user_email):
    """Ritorna tutti i profili associati a un determinato utente."""
    try:
        if not user_email:
            raise ValueError("Email dell'utente non fornita.")

        user_id = get_user_id(user_email)
        if not user_id:
            raise ValueError(f"L'utente con email {user_email} non esiste.")

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM profiles WHERE user_id = ?", (user_id,))
            profiles = cursor.fetchall()
            return profiles
    except Exception as e:
        raise ValueError(f"Errore durante il recupero dei profili: {e}")

# Funzione per caricare un profilo specifico
def load_profile(profile_id):
    """Carica i dati di un profilo specifico."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT data FROM profiles WHERE id = ?", (profile_id,))
            result = cursor.fetchone()
            return json.loads(result[0]) if result else None
    except Exception as e:
        raise ValueError(f"Errore durante il caricamento del profilo: {e}")

# Funzione per eliminare un profilo
def delete_profile(profile_id):
    """Elimina un profilo dal database."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM profiles WHERE id = ?", (profile_id,))
            conn.commit()
    except Exception as e:
        raise ValueError(f"Errore durante l'eliminazione del profilo: {e}")
