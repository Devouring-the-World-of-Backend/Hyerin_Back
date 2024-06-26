from sqlalchemy.orm import Session

from . import models, schemas

# Read a single user by ID
def get_user(db: Session, user_id = int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# Read a single user by email
def get_user_by_email(db: Session, email:str):
    return db.query(models.User).filter(models.User.email == email).first()

# Read multiple users
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

# Read multiple items
def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Book).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email = user.email, hashed_password = fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_user_book(db: Session, item:schemas.BookCreate, user_id: int):
    db_book = models.Book(**item.dict(), owner_id = user_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
