from fastapi import FastAPI, Depends, HTTPException, status, APIRouter, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
from datetime import timedelta
import os
import shutil
import uuid
import logging

from app import models, schemas, crud, auth
from app.database import engine, get_db

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ensure uploads directory exists
os.makedirs("uploads", exist_ok=True)

app = FastAPI(title="Professional Portfolio API", version="2.0.0")

@app.on_event("startup")
def startup_db_setup():
    logger.info("Initializing database...")
    try:
        # Create tables
        models.Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables verified/created.")
        
        # Ensure default admin user exists
        db = next(get_db())
        admin_username = "admin@example.com"
        admin = crud.get_user_by_username(db, admin_username)
        if not admin:
            logger.info(f"Creating default admin user: {admin_username}")
            crud.create_user(db, schemas.AdminUserCreate(username=admin_username, password="admin123"))
            logger.info(f"✅ Default admin created ({admin_username} / admin123)")
        db.close()
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")

# Mount uploads directory
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Setup CORS
origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:5175",
    "http://localhost:5176",
    "http://localhost:3000",
    "https://portfolio-vert-zeta-35.vercel.app",
    os.getenv("FRONTEND_URL", "https://portfolio-vert-zeta-35.vercel.app")
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Authentication Route
@app.post("/api/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Public API routes for portfolio data
public_router = APIRouter(prefix="/api/public", tags=["public"])

@public_router.get("/personal-profile", response_model=schemas.PersonalProfileResponse)
def read_personal_profile(db: Session = Depends(get_db)):
    res = crud.get_singleton(db, models.PersonalProfile)
    if not res: raise HTTPException(status_code=404, detail="Not found")
    return res

@public_router.get("/about", response_model=schemas.AboutSectionResponse)
def read_about_section(db: Session = Depends(get_db)):
    res = crud.get_singleton(db, models.AboutSection)
    if not res: raise HTTPException(status_code=404, detail="Not found")
    return res

@public_router.get("/social-links", response_model=List[schemas.SocialLinkResponse])
def read_social_links(db: Session = Depends(get_db)):
    return crud.get_all(db, models.SocialLink)

@public_router.get("/skills", response_model=List[schemas.SkillResponse])
def read_skills(db: Session = Depends(get_db)):
    return crud.get_all(db, models.Skill)

@public_router.get("/projects", response_model=List[schemas.ProjectResponse])
def read_projects(db: Session = Depends(get_db)):
    return crud.get_all(db, models.Project)

@public_router.get("/experience", response_model=List[schemas.ExperienceResponse])
def read_experience(db: Session = Depends(get_db)):
    return crud.get_all(db, models.Experience)

@public_router.get("/education", response_model=List[schemas.EducationResponse])
def read_education(db: Session = Depends(get_db)):
    return crud.get_all(db, models.Education)

@public_router.get("/achievements", response_model=List[schemas.AchievementResponse])
def read_achievements(db: Session = Depends(get_db)):
    return crud.get_all(db, models.Achievement)

app.include_router(public_router)

# Admin API routes (Protected)
admin_router = APIRouter(prefix="/api/admin", tags=["admin"], dependencies=[Depends(auth.get_current_user)])

@admin_router.post("/upload")
def upload_file(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1]
    filename = f"{uuid.uuid4()}{ext}"
    file_location = f"uploads/{filename}"
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    base_url = os.getenv('BACKEND_URL', 'http://127.0.0.1:8000').rstrip('/')
    return {"url": f"{base_url}/{file_location}"}

@admin_router.put("/personal-profile", response_model=schemas.PersonalProfileResponse)
def update_personal_profile(info: schemas.PersonalProfileCreate, db: Session = Depends(get_db)):
    return crud.update_singleton(db, models.PersonalProfile, info)

@admin_router.put("/about", response_model=schemas.AboutSectionResponse)
def update_about_section(info: schemas.AboutSectionCreate, db: Session = Depends(get_db)):
    return crud.update_singleton(db, models.AboutSection, info)

# Generator for CRUD endpoints
def setup_crud_endpoints(router, path, model, create_schema, response_schema):
    @router.post(f"/{path}", response_model=response_schema)
    def create_item(item: create_schema, db: Session = Depends(get_db)):
        return crud.create_item(db, model, item)

    @router.put(f"/{path}/{{id}}", response_model=response_schema)
    def update_item(id: int, item: create_schema, db: Session = Depends(get_db)):
        updated = crud.update_item(db, model, id, item)
        if not updated: raise HTTPException(status_code=404)
        return updated

    @router.delete(f"/{path}/{{id}}")
    def delete_item(id: int, db: Session = Depends(get_db)):
        if not crud.delete_item(db, model, id): raise HTTPException(status_code=404)
        return {"message": "Deleted successfully"}

setup_crud_endpoints(admin_router, "projects", models.Project, schemas.ProjectCreate, schemas.ProjectResponse)
setup_crud_endpoints(admin_router, "skills", models.Skill, schemas.SkillCreate, schemas.SkillResponse)
setup_crud_endpoints(admin_router, "experience", models.Experience, schemas.ExperienceCreate, schemas.ExperienceResponse)
setup_crud_endpoints(admin_router, "education", models.Education, schemas.EducationCreate, schemas.EducationResponse)
setup_crud_endpoints(admin_router, "achievements", models.Achievement, schemas.AchievementCreate, schemas.AchievementResponse)
setup_crud_endpoints(admin_router, "social-links", models.SocialLink, schemas.SocialLinkCreate, schemas.SocialLinkResponse)

app.include_router(admin_router)

@app.get("/")
def root():
    return {"message": "Portfolio API v2.0 is running."}
