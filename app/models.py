from sqlalchemy import Column, Integer, String, Text, Boolean, JSON
from app.database import Base

class AdminUser(Base):
    __tablename__ = "admin_users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class PersonalProfile(Base):
    __tablename__ = "personal_profile"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    title = Column(String)
    tagline = Column(String)
    email = Column(String)
    phone = Column(String)
    location = Column(String)
    date_of_birth = Column(String, nullable=True)
    fathers_name = Column(String, nullable=True)
    nationality = Column(String, nullable=True)
    profile_image_url = Column(String, nullable=True)

class AboutSection(Base):
    __tablename__ = "about_section"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, default="About Me")
    description = Column(Text)
    image_url = Column(String, nullable=True)
    resume_url = Column(String, nullable=True)
    email = Column(String, nullable=True)
    location = Column(String, nullable=True)

class SocialLink(Base):
    __tablename__ = "social_links"
    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String)
    url = Column(String)
    icon_class = Column(String, nullable=True)

class Skill(Base):
    __tablename__ = "skills"
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String)
    name = Column(String)
    proficiency = Column(Integer, nullable=True)
    icon_class = Column(String, nullable=True)
    icon_url = Column(String, nullable=True)

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(Text)
    image_url = Column(String)
    tags = Column(String)
    live_link = Column(String, nullable=True)
    github_link = Column(String, nullable=True)
    featured = Column(Boolean, default=False)

class Experience(Base):
    __tablename__ = "experience"
    id = Column(Integer, primary_key=True, index=True)
    role = Column(String)
    company = Column(String)
    duration = Column(String)
    description = Column(Text)

class Education(Base):
    __tablename__ = "education"
    id = Column(Integer, primary_key=True, index=True)
    degree = Column(String)
    institution = Column(String)
    duration = Column(String)
    description = Column(Text)

class Achievement(Base):
    __tablename__ = "achievements"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    issuer = Column(String)
    date = Column(String)
    description = Column(Text)
