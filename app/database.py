import os

from dotenv import load_dotenv

from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker, DeclarativeBase


# Load variables from the .env file
load_dotenv()

# Get the PostgreSQL connection URL from .env
DATABASE_URL = os.getenv("DATABASE_URL")


# Create the SQLAlchemy engine
# The new PostgreSQL database uses UTF-8 encoding
engine = create_engine(DATABASE_URL)


# Factory used to create database sessions
SessionLocal = sessionmaker(bind=engine)


# Base class for all SQLAlchemy models
class Base(DeclarativeBase):
    pass