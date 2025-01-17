import sqlite3
import os

# Percorso del database
DB_PATH = os.path.join(os.getcwd(), "app_data.db")

# Connessione al database
def get_connection():
    return sqlite3.connect(DB_PATH)

# Creazione delle tabelle
def initialize_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        # Tabella utenti
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        # Tabella profili
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            data TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
        """)
        conn.commit()

# Funzione per registrare un utente
def register(email, password):
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (email, password) VALUES (?, ?)", 
                (email, password)
            )
            conn.commit()  # Salva i dati nel database
            print(f"Utente registrato: {email}")  # Debug
            return True
        except sqlite3.IntegrityError as e:
            print(f"Errore durante la registrazione: {e}")  # Debug
            return False  # L'email è già registrata

# Funzione per autenticare un utente
def login(email, password):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE email = ? AND password = ?", 
            (email, password)
        )
        user = cursor.fetchone()
        return user is not None

# Funzione di debug per verificare gli utenti nel database
def debug_check_users():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        return users

# Inizializza il database
initialize_db()
