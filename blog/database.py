from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os as process
SQLALCHEMY_DATABASE_URL = process.getenv("DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


