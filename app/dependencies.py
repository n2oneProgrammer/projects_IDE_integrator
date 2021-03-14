import os
import random
import secrets

from fastapi.security import OAuth2PasswordBearer

from app.database import SessionLocal

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

SECRET_KEY = os.environ.get("secretKey")
if SECRET_KEY is None:
    SECRET_KEY = secrets.token_hex(32)

SECRET_SALT = os.environ.get("secretSalt")
if SECRET_SALT is None:
    SECRET_SALT = ""
    for i in range(16):
        SECRET_SALT += random.choice(ALPHABET)

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
