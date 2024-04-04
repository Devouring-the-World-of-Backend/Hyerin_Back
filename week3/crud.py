from sqlalchemy.orm import Session

from . import models, schemas

# Read a single user by ID
def get_user(db: Session, user_id = int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# Read a single user by email
def get_user_by_email(db: Session, email:Str)
    return db.query(models.User).filter(models.User.email == email).first()

# Read multiple users
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

# Read multiple items
def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Book).offset(skip).limit(limit).all()