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

# Inizializza il database
initialize_db()
