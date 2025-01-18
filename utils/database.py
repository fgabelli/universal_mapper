import os
import sqlite3

# Percorso del database SQLite
DATABASE_PATH = "universal_mapper.db"

# Connessione al database
def get_connection():
    """Crea una connessione al database SQLite."""
    return sqlite3.connect(DATABASE_PATH)

# Creazione delle tabelle
def initialize_db():
    """Inizializza il database e crea le tabelle necessarie."""
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
    """Registra un nuovo utente nel database."""
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (email, password) VALUES (?, ?)", 
                (email, password)
            )
            conn.commit()  # Salva i dati nel database
            return True
        except sqlite3.IntegrityError:
            return False  # L'email è già registrata

# Funzione per autenticare un utente
def login(email, password):
    """Autentica un utente con email e password."""
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
    """Restituisce tutti gli utenti registrati nel database."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, email, created_at FROM users")
        users = cursor.fetchall()
        return users

# Inizializza il database all'avvio del modulo
initialize_db()
