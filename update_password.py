import psycopg2
import hashlib

# Stringa di connessione al database di Supabase
DB_URL = "postgresql://postgres:Frabicom%2C2010@db.tgnezgsfcrzsjleokswu.supabase.co:5432/postgres"

# Funzione per generare l'hash
def hash_password(password):
    """Genera un hash SHA-256 per la password."""
    return hashlib.sha256(password.encode()).hexdigest()

# Dati dell'utente
email = "f.gabelli@gmail.com"
password = "Sup3ech80"
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
