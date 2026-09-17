import os

from sqlalchemy import create_engine, false 
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv

load_dotenv()

DB_USER= os.getenv("POSTGRES_USER")
DB_PASSWORD= os.getenv("POSTGRES_PASSWORD")
DB_HOST= os.getenv("POSTGRES_HOST")
DB_PORT= os.getenv("POSTGRES_PORT")
DB_NAME= os.getenv("POSTGRES_NAME")

DATABASE_URL = f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

print('Conectado a:', DATABASE_URL)

engine = create_engine(DATABASE_URL, echo=True, future=True)

SessionLocal = sessionmaker(bind=engine, autoflush=false, class_=Session)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()