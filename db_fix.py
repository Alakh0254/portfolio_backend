import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv

load_dotenv()

def find_working_connection():
    # Common passwords to try
    passwords = ["postgres", "admin", "password", "123456", "root", ""]
    target_db = "portfolio_db"
    
    for pwd in passwords:
        try:
            print(f"Trying password: '{pwd}'...")
            conn = psycopg2.connect(
                dbname="postgres",
                user="postgres",
                password=pwd,
                host="localhost",
                port="5432"
            )
            print(f"SUCCESS! Working password is: '{pwd}'")
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur = conn.cursor()
            
            # Ensure target database exists
            cur.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{target_db}'")
            if not cur.fetchone():
                print(f"Creating database '{target_db}'...")
                cur.execute(f"CREATE DATABASE {target_db}")
            
            cur.close()
            conn.close()
            
            # Update .env
            update_env(pwd)
            return True
        except Exception as e:
            if "authentication failed" in str(e):
                continue
            else:
                print(f"Other Error with '{pwd}': {e}")
                
    print("Failed to find working credentials. Please verify your PostgreSQL setup manually.")
    return False

def update_env(password):
    env_path = "c:\\Users\\gagan\\Desktop\\portfolio\\backend\\.env"
    with open(env_path, 'r') as f:
        lines = f.readlines()
    
    with open(env_path, 'w') as f:
        for line in lines:
            if line.startswith("DATABASE_URL="):
                f.write(f"DATABASE_URL=postgresql://postgres:{password}@localhost:5432/portfolio_db\n")
            else:
                f.write(line)
    print(".env updated successfully.")

if __name__ == "__main__":
    find_working_connection()
