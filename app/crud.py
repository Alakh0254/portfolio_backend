from sqlalchemy.orm import Session
from app import models, schemas, auth

# User CRUD
def get_user_by_username(db: Session, username: str):
    return db.query(models.AdminUser).filter(models.AdminUser.username == username).first()

def create_user(db: Session, user: schemas.AdminUserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.AdminUser(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Generic CRUD factory functions
def get_all(db: Session, model):
    return db.query(model).all()

def get_by_id(db: Session, model, item_id: int):
    return db.query(model).filter(model.id == item_id).first()

def create_item(db: Session, model, item):
    db_item = model(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_item(db: Session, model, item_id: int, item_data):
    db_item = db.query(model).filter(model.id == item_id).first()
    if db_item:
        for key, value in item_data.model_dump().items():
            setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)
    return db_item

def delete_item(db: Session, model, item_id: int):
    db_item = db.query(model).filter(model.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
        return True
    return False

# Specifically for Singleton-like sections (Profile, About)
def get_singleton(db: Session, model):
    return db.query(model).first()

def update_singleton(db: Session, model, item_data):
    db_item = db.query(model).first()
    if db_item:
        for key, value in item_data.model_dump().items():
            setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)
        return db_item
    else:
        db_item = model(**item_data.model_dump())
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
