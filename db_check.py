import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv

load_dotenv()

def diagnostic():
    db_url = os.getenv("DATABASE_URL")
    print(f"Checking connection to: {db_url}")
    
    # Extract connection info
    try:
        # Try to connect to 'postgres' database first to see if we can authenticate
        # We replace the DB name in the URL with 'postgres'
        base_url = db_url.rsplit('/', 1)[0] + '/postgres'
        
        print(f"Attempting to authenticate with 'postgres' system database...")
        conn = psycopg2.connect(base_url)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        
        # Check if our target database exists
        target_db = db_url.rsplit('/', 1)[1]
        cur.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{target_db}'")
        exists = cur.fetchone()
        
        if not exists:
            print(f"Database '{target_db}' does not exist. Creating it...")
            cur.execute(f"CREATE DATABASE {target_db}")
            print(f"Database '{target_db}' created successfully.")
        else:
            print(f"Database '{target_db}' already exists.")
            
        cur.close()
        conn.close()
        print("PostgreSQL connection and database verification successful.")
        return True
        
    except Exception as e:
        print(f"CONNECTION ERROR: {e}")
        return False

if __name__ == "__main__":
    diagnostic()
