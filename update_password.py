import psycopg2
import hashlib
import os

# Ottieni la stringa di connessione al database dai secrets o dalle variabili di ambiente
DB_URL = os.getenv("DB_URL")

# Funzione per generare l'hash
def hash_password(password):
    """Genera un hash SHA-256 per la password."""
    return hashlib.sha256(password.encode()).hexdigest()

# Richiedi i dati dell'utente in modo interattivo
email = input("Inserisci l'email dell'utente: ")
password = input("Inserisci la nuova password: ")

# Genera l'hash della password
hashed_password = hash_password(password)

# Aggiorna la password nel database
try:
    with psycopg2.connect(DB_URL) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE users SET password = %s WHERE email = %s",
                (hashed_password, email),
            )
            conn.commit()
            print("Password aggiornata con successo!")
except Exception as e:
    print(f"Errore durante l'aggiornamento della password: {e}")
