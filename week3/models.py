from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key = True)
    title = Column(String, index = True)
    author = Column(String, index = True)
    description = Column(String, index = True)
    published_year = Column(Integer)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True)
    owner_id = Column(Integer, ForeignKey("books.id"))

    owner = relationship("Book", back_populates="users")