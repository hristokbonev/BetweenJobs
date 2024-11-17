import os
from typing import Optional
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from sqlmodel import Session, select
from data.database import get_session
from data.db_models import User



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/token/login")

key = os.getenv("SECRET_KEY")
algorithm = os.getenv("ALGORITHM")
access_token_expire_minutes = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=access_token_expire_minutes))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, key, algorithm=algorithm)


def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, key, algorithms=[algorithm])
        return payload
    except JWTError:
        return None
    

def authenticate_user(session: Session, username: str, password: str) -> Optional[User]:
    statement = select(User).where(User.username == username)
    user = session.execute(statement).scalars().first()

    if user and verify_password(password, user.password):
        return user
    return None


def get_current_user(
    token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)) -> User:
    try:
        payload = jwt.decode(token, key, algorithms=[algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    statement = select(User).where(User.username == username)
    user = session.execute(statement).scalars().first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

