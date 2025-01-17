import json
import os
import sqlite3
from utils.database import get_connection

# Percorso del file JSON di backup (opzionale, per la migrazione)
PROFILES_BACKUP_FILE = os.path.join(os.path.dirname(__file__), "profiles_backup.json")

# Funzione per salvare un profilo per un utente specifico nel database
def save_profile(user_id, profile_name, associations):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO profiles (user_id, name, data) VALUES (?, ?, ?)",
            (user_id, profile_name, json.dumps(associations))
        )
        conn.commit()

# Funzione per caricare tutti i profili per un utente specifico
def list_profiles(user_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM profiles WHERE user_id = ?", (user_id,))
        return cursor.fetchall()

# Funzione per caricare un profilo specifico
def load_profile(profile_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT data FROM profiles WHERE id = ?", (profile_id,))
        result = cursor.fetchone()
        return json.loads(result[0]) if result else None

# Funzione per eliminare un profilo specifico
def delete_profile(profile_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM profiles WHERE id = ?", (profile_id,))
        conn.commit()

# Funzione di backup: salva i profili in un file JSON (opzionale)
def backup_profiles():
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

# Funzione di ripristino: carica i profili da un file JSON nel database (opzionale)
def restore_profiles():
    if not os.path.exists(PROFILES_BACKUP_FILE):
        return

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
