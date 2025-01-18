import sqlite3
import os

# Percorso del file del database SQLite
DB_PATH = os.path.join(os.path.dirname(__file__), "database.sqlite")

# Connessione al database SQLite
def get_connection():
    return sqlite3.connect(DB_PATH)

# Inizializza il database
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
