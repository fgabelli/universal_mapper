import json
import sqlite3
from utils.database import get_connection

# Funzione per ottenere l'ID dell'utente dato l'email
def get_user_id(email):
    if not email:
        raise ValueError("Email non fornita. Assicurati che l'utente sia autenticato.")

    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
            result = cursor.fetchone()
            return result[0] if result else None
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
    if not user_email:
        st.error("Email dell'utente non fornita. Assicurati che l'utente sia autenticato.")
        return []

    try:
        user_id = get_user_id(user_email)
        if not user_id:
            st.warning(f"Nessun profilo caricato: utente {user_email} non trovato.")
            return []

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM profiles WHERE user_id = ?", (user_id,))
            profiles = cursor.fetchall()
            return profiles
    except Exception as e:
        st.error(f"Errore durante il recupero dei profili: {e}")
        return []

# Funzione per eliminare un profilo specifico
def delete_profile(profile_id):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM profiles WHERE id = ?", (profile_id,))
            conn.commit()
    except Exception as e:
        raise ValueError(f"Errore durante l'eliminazione del profilo: {e}")
