import sqlite3
import sqlalchemy
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os
import sys

# Add the current directory to sys.path to import app
sys.path.append(os.getcwd())

from app import models
from app.database import Base, engine, SessionLocal

def migrate():
    print("Starting migration to Supabase...")
    
    # 1. Ensure tables exist in Supabase
    print("Creating tables in Supabase (if they don't exist)...")
    models.Base.metadata.create_all(bind=engine)
    
    # Destination session
    dest_session = SessionLocal()
    
    print("Clearing existing data in Supabase...")
    try:
        dest_session.execute(text("TRUNCATE TABLE personal_profile, projects, skills, experience, education, achievements, social_links RESTART IDENTITY CASCADE"))
        dest_session.commit()
    except Exception as e:
        dest_session.rollback()
        # Fallback for if TRUNCATE fails or tables don't exist
        print(f"Clear failed (might be first run): {e}")

    # 2. Connect to source (SQLite)
    # We'll use SQLite as the primary source since we know it has data
    source_db = 'portfolio.db'
    if not os.path.exists(source_db):
        print(f"Source database {source_db} not found.")
        return

    sqlite_conn = sqlite3.connect(source_db)
    sqlite_conn.row_factory = sqlite3.Row
    sqlite_cursor = sqlite_conn.cursor()

    try:
        # Migrate Personal Info -> PersonalProfile
        print("Migrating Personal Profile...")
        sqlite_cursor.execute("SELECT * FROM personal_info")
        rows = sqlite_cursor.fetchall()
        for row in rows:
            # Check if exists
            exists = dest_session.query(models.PersonalProfile).first()
            if not exists:
                profile = models.PersonalProfile(
                    name=row['name'],
                    title=row['title'],
                    tagline=row['tagline'],
                    email=row['email'],
                    phone=row['phone'],
                    location=row['location'],
                    profile_image_url=row['profile_image_url']
                )
                dest_session.add(profile)
        
        # Migrate Projects
        print("Migrating Projects...")
        sqlite_cursor.execute("SELECT * FROM projects")
        rows = sqlite_cursor.fetchall()
        for row in rows:
            project = models.Project(
                title=row['title'],
                description=row['description'],
                image_url=row['image_url'],
                tags=row['tags'],
                live_link=row['live_link'],
                github_link=row['github_link'],
                featured=bool(row['featured'])
            )
            dest_session.add(project)

        # Migrate Skills
        print("Migrating Skills...")
        sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='skills'")
        if sqlite_cursor.fetchone():
            sqlite_cursor.execute("SELECT * FROM skills")
            for row in sqlite_cursor.fetchall():
                skill = models.Skill(
                    category=row['category'],
                    name=row['name'],
                    proficiency=row['proficiency'],
                    icon_class=row['icon_class']
                )
                dest_session.add(skill)

        # Migrate Experience
        print("Migrating Experience...")
        sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='experience'")
        if sqlite_cursor.fetchone():
            sqlite_cursor.execute("SELECT * FROM experience")
            for row in sqlite_cursor.fetchall():
                exp = models.Experience(
                    role=row['role'],
                    company=row['company'],
                    duration=row['duration'],
                    description=row['description']
                )
                dest_session.add(exp)

        # Migrate Education
        print("Migrating Education...")
        sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='education'")
        if sqlite_cursor.fetchone():
            sqlite_cursor.execute("SELECT * FROM education")
            for row in sqlite_cursor.fetchall():
                edu = models.Education(
                    degree=row['degree'],
                    institution=row['institution'],
                    duration=row['duration'],
                    description=row['description']
                )
                dest_session.add(edu)

        # Migrate Achievements
        print("Migrating Achievements...")
        sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='achievements'")
        if sqlite_cursor.fetchone():
            sqlite_cursor.execute("SELECT * FROM achievements")
            for row in sqlite_cursor.fetchall():
                ach = models.Achievement(
                    title=row['title'],
                    issuer=row['issuer'],
                    date=row['date'],
                    description=row['description']
                )
                dest_session.add(ach)

        # Migrate Social Links
        print("Migrating Social Links...")
        sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='social_links'")
        if sqlite_cursor.fetchone():
            sqlite_cursor.execute("SELECT * FROM social_links")
            for row in sqlite_cursor.fetchall():
                social = models.SocialLink(
                    platform=row['platform'],
                    url=row['url'],
                    icon_class=row['icon_class']
                )
                dest_session.add(social)
        
        dest_session.commit()
        print("Migration completed successfully!")
        
    except Exception as e:
        dest_session.rollback()
        print(f"Migration failed: {e}")
    finally:
        sqlite_conn.close()
        dest_session.close()

if __name__ == "__main__":
    migrate()
