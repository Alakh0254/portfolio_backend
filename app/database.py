from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import sys
import logging
from dotenv import load_dotenv

load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")

# Production fix for postgres:// vs postgresql://
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

if not DATABASE_URL:
    logger.error("DATABASE_URL not found in .env file!")
    # Template fallback
    DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/portfolio_db"

logger.info(f"Connecting to database at {DATABASE_URL.split('@')[-1]}...")

try:
    engine = create_engine(DATABASE_URL)
    # Immediate connection test
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    logger.info("✅ PostgreSQL connection established successfully.")
except Exception as e:
    logger.error("❌ Failed to connect to PostgreSQL!")
    logger.error(f"Error Details: {e}")
    logger.warning("Please ensure:")
    logger.warning("1. PostgreSQL is running.")
    logger.warning("2. The 'portfolio_db' database exists (or you have permissions to create it).")
    logger.warning("3. Your credentials in .env are correct.")
    # We don't exit here to allow FastAPI to show startup errors properly
    # but we initialize engine anyway
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
