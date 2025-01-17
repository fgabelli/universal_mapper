import json
import os

# Percorso del file JSON dove sono salvati i profili
PROFILES_FILE = os.path.join(os.path.dirname(__file__), "profiles.json")

# Carica tutti i profili dal file JSON
def load_all_profiles():
    if not os.path.exists(PROFILES_FILE):
        return {}
    with open(PROFILES_FILE, "r") as file:
        return json.load(file)

# Salva tutti i profili nel file JSON
def save_all_profiles(profiles):
    with open(PROFILES_FILE, "w") as file:
        json.dump(profiles, file, indent=4)

# Elenco dei profili per un utente specifico
def list_profiles(user_email):
    profiles = load_all_profiles()
    return profiles.get(user_email, {}).keys()

# Salva un profilo per un utente specifico
def save_profile(profile_name, associations, user_email):
    profiles = load_all_profiles()
    if user_email not in profiles:
        profiles[user_email] = {}
    profiles[user_email][profile_name] = associations
    save_all_profiles(profiles)

# Carica un profilo per un utente specifico
def load_profile(profile_name, user_email):
    profiles = load_all_profiles()
    return profiles.get(user_email, {}).get(profile_name)

# Elimina un profilo per un utente specifico
def delete_profile(profile_name, user_email):
    profiles = load_all_profiles()
    if user_email in profiles and profile_name in profiles[user_email]:
        del profiles[user_email][profile_name]
        if not profiles[user_email]:  # Rimuovi l'utente se non ha più profili
            del profiles[user_email]
        save_all_profiles(profiles)
