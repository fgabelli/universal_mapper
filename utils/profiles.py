import json
from utils.database import get_connection

# Funzione per ottenere l'ID dell'utente dato l'email
def get_user_id(email):
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            result = cursor.fetchone()
            if result:
                return result[0]
            return None
        except Exception as e:
            raise ValueError(f"Errore durante il recupero dell'ID utente: {e}")

# Funzione per salvare un profilo
def save_profile(user_id, profile_name, associations):
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO profiles (user_id, name, data) VALUES (%s, %s, %s)",
                (user_id, profile_name, json.dumps(associations))
            )
            conn.commit()
        except Exception as e:
            raise ValueError(f"Errore durante il salvataggio del profilo: {e}")

# Funzione per caricare tutti i profili di un utente
def list_profiles(user_email):
    user_id = get_user_id(user_email)
    if not user_id:
        return []
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, name FROM profiles WHERE user_id = %s", (user_id,))
            return cursor.fetchall()
        except Exception as e:
            raise ValueError(f"Errore durante il recupero dei profili: {e}")

# Funzione per caricare un profilo specifico
def load_profile(profile_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT data FROM profiles WHERE id = %s", (profile_id,))
            result = cursor.fetchone()
            return json.loads(result[0]) if result else None
        except Exception as e:
            raise ValueError(f"Errore durante il caricamento del profilo: {e}")

# Funzione per eliminare un profilo
def delete_profile(profile_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM profiles WHERE id = %s", (profile_id,))
            conn.commit()
        except Exception as e:
            raise ValueError(f"Errore durante l'eliminazione del profilo: {e}")
