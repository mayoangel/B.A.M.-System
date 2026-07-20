# app/core/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from flask import g 
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    if 'db' not in g:
        g.db = SessionLocal()
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()