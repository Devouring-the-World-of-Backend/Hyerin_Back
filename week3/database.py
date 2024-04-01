from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# PostgreSQL: SQLALCHEMY_dATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connet_args={"check_same_thread": False}
    )
