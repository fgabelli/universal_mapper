import json
import os

PROFILES_FILE = "profiles.json"

def save_profile(profile_name, associations):
    profiles = {}
    if os.path.exists(PROFILES_FILE):
        with open(PROFILES_FILE, "r") as file:
            profiles = json.load(file)
    profiles[profile_name] = associations
    with open(PROFILES_FILE, "w") as file:
        json.dump(profiles, file)

def load_profile(profile_name):
    if os.path.exists(PROFILES_FILE):
        with open(PROFILES_FILE, "r") as file:
            profiles = json.load(file)
        return profiles.get(profile_name, [])
    return []

def list_profiles():
    if os.path.exists(PROFILES_FILE):
        with open(PROFILES_FILE, "r") as file:
            profiles = json.load(file)
        return list(profiles.keys())
    return []

def delete_profile(profile_name):
    if os.path.exists(PROFILES_FILE):
        with open(PROFILES_FILE, "r") as file:
            profiles = json.load(file)
        if profile_name in profiles:
            del profiles[profile_name]
            with open(PROFILES_FILE, "w") as file:
                json.dump(profiles, file)
