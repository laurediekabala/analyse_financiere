import streamlit as st
import sqlite3
import bcrypt # Pour hacher les mots de passe
from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "sqlite:///./data/users.db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    username = Column(String, primary_key=True, unique=True, index=True)
    hashed_password = Column(String)

# Créer la table si elle n'existe pas
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_user(username, password):
    db = SessionLocal()
    try:
        if db.query(User).filter(User.username == username).first():
            return False # User already exists
        hashed = hash_password(password)
        new_user = User(username=username, hashed_password=hashed)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return True
    finally:
        db.close()

def authenticate_user(username, password):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        if user and verify_password(password, user.hashed_password):
            return True
        return False
    finally:
        db.close()

# Initialisation d'un utilisateur admin pour le premier démarrage
def init_admin_user():
    db = SessionLocal()
    try:
        if not db.query(User).filter(User.username == "admin").first():
            hashed = hash_password("admin") # Mot de passe par défaut pour admin
            admin_user = User(username="admin", hashed_password=hashed)
            db.add(admin_user)
            db.commit()
            print("Admin user 'admin' created with password 'admin'")
    finally:
        db.close()

# Appeler cette fonction une fois au démarrage de l'app si besoin
init_admin_user()