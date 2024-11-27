from datetime import datetime, timedelta
import os
from typing import Optional
from jose import jwt, JWTError
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlmodel import Session
from data.database import engine
from utils.crud import get_user, get_user_by_username


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/users/login', auto_error=False)


key = os.getenv("SECRET_KEY")
algorithm = os.getenv("ALGORITHM")
access_token_expire_minutes = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

token_blacklist = set()

def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(username: str, password: str):
    with Session(engine) as session:
        user = get_user_by_username(session, username)
        if not user or not verify_password(password, user.password):
            return None
        return user

def create_access_token(data:dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes= int(access_token_expire_minutes))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, key, algorithm=algorithm)
    return encoded_jwt

def verify_token(token: str):
    if token in token_blacklist:
        raise HTTPException(status_code=401, detail="Token has been revoked")

    if not token:
        return None

    try:
        payload = jwt.decode(token, key, algorithms=[algorithm])
        username = payload.get('sub') if payload else None
        if username is None:
            return None
        return payload
    except JWTError:
            return None


def get_current_user(token: str = Depends(oauth2_scheme)):
    if not token:
        return None
    payload = verify_token(token)
    username = payload.get('sub') if payload else None
    if not username:
        return None
    return get_user(username, session=Session(engine))
