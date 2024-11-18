import os
from fastapi import APIRouter, FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from data.db_models import User
from users import auth
from users.crud import get_user_by_username
from users.user_models import UserCreate, UserSchema, Token, TokenData, UserUpdate
from users.auth import verify_password, create_access_token, get_current_user, get_password_hash
from data.database import engine, create_db
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta

users_router = APIRouter(prefix='/api/users', tags=["Users"])

key = os.getenv("SECRET_KEY")
algorithm = os.getenv("ALGORITHM")
access_token_expire_minutes = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

create_db()

def get_session():
    with Session(engine) as session:
        yield session


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/users/login', auto_error=False)   

@users_router.post('/', response_model=UserSchema)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    db_user = User( username=user.username,
                    password=get_password_hash(user.password),
                    first_name=user.first_name,
                    last_name=user.last_name,
                    is_admin=user.is_admin,
                    date_of_birth=user.birth_date,
                    email=user.email
                )
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@users_router.put('/{user_id}', response_model=UserSchema)
def update_user(user_id: int, user: UserUpdate, session: Session = Depends(get_session)):
    user = session.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user.username = user.username
    user.password = get_password_hash(user.password)
    user.first_name = user.first_name
    user.last_name = user.last_name
    user.email = user.email
    session.commit()
    session.refresh(user)
    return user


@users_router.delete('/{user_id}', response_model=UserSchema)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user = session.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    session.delete(user)
    session.commit()
    return user


@users_router.post('/login', response_model=Token)
def login(from_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = auth.authenticate_user(from_data.username, from_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    is_admin = user.is_admin
    id = user.id
    access_token = create_access_token(data={'sub': user.username, 'is_admin': is_admin, "id": id})

    return Token(access_token=access_token, token_type="bearer")
    


@users_router.post('/logout')
def logout(token: str = Depends(oauth2_scheme)):
    auth.verify_token(token)
    auth.token_blacklist.add(token)
    return {"message": "Successfully logged out"}