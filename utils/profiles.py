import json
import os
import sqlite3
import streamlit as st
from utils.database import get_connection

# Percorso del file JSON di backup (opzionale)
PROFILES_BACKUP_FILE = os.path.join(os.path.dirname(__file__), "profiles_backup.json")

# Funzione per ottenere l'ID dell'utente dato l'email
def get_user_id(email):
    """Ottiene l'ID dell'utente dato l'email."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
            user = cursor.fetchone()
            return user[0] if user else None
    except sqlite3.Error as e:
        st.error(f"Errore durante il recupero dell'ID utente: {e}")
        return None

# Funzione per salvare un profilo per un utente specifico nel database
def save_profile(user_id, profile_name, associations):
    """Salva un profilo nel database SQLite."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO profiles (user_id, name, data) VALUES (?, ?, ?)",
                (user_id, profile_name, json.dumps(associations))
            )
            conn.commit()
            st.success(f"Profilo '{profile_name}' salvato con successo!")
    except sqlite3.Error as e:
        st.error(f"Errore durante il salvataggio del profilo: {e}")
# Funzione per caricare tutti i profili per un utente specifico
def list_profiles(user_email):
    """Restituisce l'elenco dei profili per un determinato utente."""
    user_id = get_user_id(user_email)
    if not user_id:
        st.warning("Nessun utente trovato.")
        return []

    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM profiles WHERE user_id = ?", (user_id,))
            profiles = cursor.fetchall()
            return profiles
    except sqlite3.Error as e:
        st.error(f"Errore durante il recupero dei profili: {e}")
        return []

# Funzione per caricare un profilo specifico
def load_profile(profile_id):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT data FROM profiles WHERE id = ?", (profile_id,))
            result = cursor.fetchone()
            return json.loads(result[0]) if result else None
    except Exception as e:
        raise ValueError(f"Errore durante il caricamento del profilo: {e}")

# Funzione per eliminare un profilo specifico
def delete_profile(profile_id):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM profiles WHERE id = ?", (profile_id,))
            conn.commit()
            st.success(f"Profilo con ID {profile_id} eliminato con successo!")
    except Exception as e:
        raise ValueError(f"Errore durante l'eliminazione del profilo: {e}")

# Funzione di backup: salva i profili in un file JSON (opzionale)
def backup_profiles():
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT user_id, name, data FROM profiles")
            profiles = cursor.fetchall()

        backup = {}
        for user_id, name, data in profiles:
            if user_id not in backup:
                backup[user_id] = {}
            backup[user_id][name] = json.loads(data)

        with open(PROFILES_BACKUP_FILE, "w") as file:
            json.dump(backup, file, indent=4)
        st.success("Backup completato con successo!")
    except Exception as e:
        raise ValueError(f"Errore durante il backup dei profili: {e}")

# Funzione di ripristino: carica i profili da un file JSON nel database (opzionale)
def restore_profiles():
    if not os.path.exists(PROFILES_BACKUP_FILE):
        st.warning("File di backup non trovato.")
        return

    try:
        with open(PROFILES_BACKUP_FILE, "r") as file:
            backup = json.load(file)

        with get_connection() as conn:
            cursor = conn.cursor()
            for user_id, profiles in backup.items():
                for name, data in profiles.items():
                    cursor.execute(
                        "INSERT INTO profiles (user_id, name, data) VALUES (?, ?, ?)",
                        (user_id, name, json.dumps(data))
                    )
            conn.commit()
        st.success("Ripristino completato con successo!")
    except Exception as e:
        raise ValueError(f"Errore durante il ripristino dei profili: {e}")
