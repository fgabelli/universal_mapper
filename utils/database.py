import os
import psycopg2
from psycopg2.extras import RealDictCursor

# URL del database PostgreSQL
DB_URL = "postgresql://postgres:Frabicom,2010@db.tgnezgsfcrzsjleokswu.supabase.co:5432/postgres"

# Connessione al database
def get_connection():
    return psycopg2.connect(DB_URL, cursor_factory=RealDictCursor)

# Creazione delle tabelle
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

# Funzione per registrare un utente
def register(email, password):
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (email, password) VALUES (%s, %s)", 
                (email, password)
            )
            conn.commit()  # Salva i dati nel database
            return True
        except psycopg2.IntegrityError:
            return False  # L'email è già registrata

# Funzione per autenticare un utente
def login(email, password):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE email = %s AND password = %s", 
            (email, password)
        )
        user = cursor.fetchone()
        return user is not None

# Funzione di debug per verificare gli utenti nel database
def debug_check_users():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, email, created_at FROM users")
        users = cursor.fetchall()
        return users

# Inizializza il database
initialize_db()
