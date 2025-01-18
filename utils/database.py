import os
import psycopg2
from psycopg2.extras import RealDictCursor

# Legge la stringa di connessione dalle variabili d'ambiente
DB_URL = os.getenv("DB_URL")

def get_connection():
    if not DB_URL:
        raise EnvironmentError("La variabile d'ambiente 'DB_URL' non è configurata.")
    return psycopg2.connect(DB_URL, cursor_factory=RealDictCursor)

def initialize_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        # Tabella utenti
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        # Tabella profili
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS profiles (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            data TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
        """)
        conn.commit()
