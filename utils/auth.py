from datetime import datetime, timedelta
import os
from typing import Optional
from jose import jwt, JWTError
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlmodel import Session, select
from data.database import engine
from data.db_models import User
from users import user_service as us



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/users/login', auto_error=False)


key = os.getenv("SECRET_KEY")
algorithm = os.getenv("ALGORITHM")
access_token_expire_minutes = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

token_blacklist = set()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(identifier: str, password: str):
    with Session(engine) as session:
        user = None
        if identifier.isdigit():  
            user = us.view_user_by_id(int(identifier), session)
        else: 
            statement = select(User).where(User.username == identifier)
            user = session.exec(statement).first()

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
    return us.get_user(username, session=Session(engine))


# def get_current_admin_user(user: User = Depends(get_current_user)):
#     if not user.is_admin:
#         raise HTTPException(status_code=403, detail="User is not an admin")
#     return user


def get_current_admin_user(token: str = Depends(oauth2_scheme)):
    user = get_current_user(token)  # Assuming this function returns a User or None
    if user is None:
        raise HTTPException(status_code=401, detail="User not authenticated")
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="User is not an admin")
    return None

