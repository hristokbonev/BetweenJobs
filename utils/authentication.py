from datetime import timedelta
import os
from fastapi import APIRouter, Depends, HTTPException, status
from data.db_models import User
from utils import auth
from users.user_models import UserCreate, UserSchema, Token, UserUpdate
from utils.auth import  create_access_token, get_password_hash, verify_password
from data.database import engine, create_db
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session, select


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
def update_user(user_id: int, user_update: UserUpdate, session: Session = Depends(get_session)):
    statement = select(User).where(User.id == user_id)
    user = session.exec(statement).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if user_update.username:
        user.username = user_update.username  # Update username
    if user_update.password:
        user.password = get_password_hash(user_update.password)  # Hash and update password
    if user_update.first_name:
        user.first_name = user_update.first_name  # Update first name
    if user_update.last_name:
        user.last_name = user_update.last_name  # Update last name
    if user_update.email:
        user.email = user_update.email  # Update email
    session.commit()
    session.refresh(user)
    return user



@users_router.post('/login', response_model=Token)
def login(from_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    statement = select(User).where(User.username == from_data.username)
    user = session.exec(statement).first()
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    # is_admin = user.is_admin
    # id = user.id
    access_token_expires = timedelta(minutes= int(access_token_expire_minutes))
    access_token = create_access_token(data={'sub': user.username},
                                        expires_delta=access_token_expires)

    return Token(access_token=access_token, token_type="bearer")
    


@users_router.post('/logout')
def logout(token: str = Depends(oauth2_scheme)):
    auth.verify_token(token)
    auth.token_blacklist.add(token)
    return {"message": "Successfully logged out"}