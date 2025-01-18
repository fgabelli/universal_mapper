import sqlite3
import os

# Ottieni il percorso del database SQLite
DB_PATH = os.getenv("DB_PATH", "database.db")

# Connessione al database
def get_connection():
    """Crea una connessione al database SQLite."""
    return sqlite3.connect(DB_PATH)

# Creazione delle tabelle nel database
def initialize_db():
    """Crea le tabelle necessarie se non esistono."""
    with get_connection() as conn:
        cursor = conn.cursor()
        # Crea la tabella utenti
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        # Crea la tabella profili
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

# Funzione di debug per verificare il contenuto delle tabelle
def debug_check_users():
    """Restituisce un elenco di utenti per il debug."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, email, created_at FROM users")
        return cursor.fetchall()

# Inizializza il database al primo avvio
initialize_db()
