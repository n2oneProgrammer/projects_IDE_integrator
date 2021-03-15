import os
import random
import secrets

from fastapi.security import OAuth2PasswordBearer

from app.database import SessionLocal

color_regex = "^[a-fA-F0-9]{6}$"


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
