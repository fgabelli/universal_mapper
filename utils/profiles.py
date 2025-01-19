import json
import sqlite3
from utils.database import get_connection

# Funzione per ottenere l'ID dell'utente dato l'email
def get_user_id(email):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                raise ValueError(f"Utente non trovato per email: {email}")
    except Exception as e:
        raise ValueError(f"Errore durante il recupero dell'ID utente: {e}")

# Funzione per salvare un profilo per un utente specifico nel database
def save_profile(user_id, profile_name, associations):
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

# Funzione per caricare tutti i profili per un utente specifico
def list_profiles(user_email):
    user_id = get_user_id(user_email)
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM profiles WHERE user_id = ?", (user_id,))
            return cursor.fetchall()
    except Exception as e:
        raise ValueError(f"Errore durante il recupero dei profili: {e}")

# Funzione per caricare un profilo specifico
def load_profile(profile_id):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT data FROM profiles WHERE id = ?", (profile_id,))
            result = cursor.fetchone()
            if result:
                return json.loads(result[0])
            else:
                raise ValueError("Profilo non trovato.")
    except Exception as e:
        raise ValueError(f"Errore durante il caricamento del profilo: {e}")

# Funzione per eliminare un profilo specifico
def delete_profile(profile_id):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM profiles WHERE id = ?", (profile_id,))
            conn.commit()
    except Exception as e:
        raise ValueError(f"Errore durante l'eliminazione del profilo: {e}")
