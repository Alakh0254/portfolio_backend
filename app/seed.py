from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app import models, auth
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def seed_data():
    db = SessionLocal()
    try:
        logger.info("Initializing database schema...")
        models.Base.metadata.create_all(bind=engine)
        
        # 1. Seed Admin User
        admin_username = "admin@example.com"
        admin = db.query(models.AdminUser).filter(models.AdminUser.username == admin_username).first()
        if not admin:
            logger.info(f"Creating admin user: {admin_username}")
            hashed_password = auth.get_password_hash("admin123")
            db.add(models.AdminUser(username=admin_username, hashed_password=hashed_password))
        else:
            logger.info("Admin user already exists.")
            
        # 2. Seed Personal Profile
        profile = db.query(models.PersonalProfile).first()
        if not profile:
            logger.info("Creating initial Personal Profile...")
            db.add(models.PersonalProfile(
                name="Alakh Singh",
                title="Software Engineer & Architect",
                tagline="Engineering high-performance digital experiences with precision.",
                email="admin@example.com",
                phone="+91 9999999999",
                location="Lucknow, India",
                date_of_birth="Jan 01, 2000",
                nationality="Indian"
            ))
            
        # 3. Seed About Section
        about = db.query(models.AboutSection).first()
        if not about:
            logger.info("Creating initial About Section...")
            db.add(models.AboutSection(
                title="System Architect & Developer",
                description="I am a passionate engineer transitioning from Electrical Engineering to Software Development. My background allows me to approach coding with a unique perspective on systems and logic.",
                email="admin@example.com",
                location="Lucknow, India"
            ))
            
        # 4. Seed Initial Skills
        if not db.query(models.Skill).first():
            logger.info("Seeding initial skills...")
            db.add(models.Skill(category="Frontend", name="React.js", proficiency=90, icon_class="html"))
            db.add(models.Skill(category="Backend", name="FastAPI", proficiency=85, icon_class="api"))
            db.add(models.Skill(category="Database", name="PostgreSQL", proficiency=80, icon_class="database"))

        # 5. Seed Initial Project
        if not db.query(models.Project).first():
            logger.info("Seeding initial project...")
            db.add(models.Project(
                title="AS.DEV Control System",
                description="A high-performance CMS for developers built with FastAPI and React.",
                image_url="https://via.placeholder.com/800x450/091517/00d2d3?text=AS.DEV+CMS",
                tags="React,FastAPI,PostgreSQL",
                featured=True
            ))

        db.commit()
        logger.info("✅ Database seeded successfully!")
    except Exception as e:
        logger.error(f"❌ Seeding failed: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
