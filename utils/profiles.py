import json
import os
from utils.database import get_connection

# Funzione per ottenere l'ID dell'utente dato l'email
def get_user_id(email):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            result = cursor.fetchone()
            if result is None:
                raise ValueError(f"Utente con email '{email}' non trovato.")
            return result[0]
    except Exception as e:
        raise ValueError(f"Errore durante il recupero dell'ID utente: {e}")

# Funzione per salvare un profilo per un utente specifico nel database
def save_profile(user_id, profile_name, associations):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO profiles (user_id, name, data) VALUES (%s, %s, %s)",
                (user_id, profile_name, json.dumps(associations)),
            )
            conn.commit()
    except Exception as e:
        raise ValueError(f"Errore durante il salvataggio del profilo: {e}")

# Funzione per caricare tutti i profili per un utente specifico
def list_profiles(user_email):
    try:
        user_id = get_user_id(user_email)
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM profiles WHERE user_id = %s", (user_id,))
            return cursor.fetchall()
    except Exception as e:
        raise ValueError(f"Errore durante il recupero dei profili: {e}")


# Funzione per eliminare un profilo
def delete_profile(profile_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM profiles WHERE id = %s", (profile_id,))
            conn.commit()
        except Exception as e:
            raise ValueError(f"Errore durante l'eliminazione del profilo: {e}")
