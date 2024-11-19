from datetime import timedelta
import os
from fastapi import APIRouter, Depends, HTTPException, status
from data.db_models import User
from users.user_service import update_user
from utils import auth
from users.user_models import UserCreate, UserSchema, Token, UserUpdate
from utils.auth import  create_access_token, get_password_hash
from data.database import engine, create_db
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session, select


router = APIRouter(prefix='/api/users', tags=["Users"])

key = os.getenv("SECRET_KEY")
algorithm = os.getenv("ALGORITHM")
access_token_expire_minutes = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

create_db()

def get_session():
    with Session(engine) as session:
        yield session


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/users/login', auto_error=False)   

@router.post('/', response_model=UserSchema)
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


@router.put('/{user_id}', response_model=UserSchema)
def update_user_info(user_id: int, user_update: UserUpdate, session: Session = Depends(get_session)):

    updated_user = update_user(user_id, user_update, session)
    if not updated_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return updated_user
    

@router.post('/login', response_model=Token)
def login(from_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    statement = select(User).where(User.username == from_data.username)
    user = session.exec(statement).first()
    
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes= int(access_token_expire_minutes))
    access_token = create_access_token(data={'sub': user.username},
                                        expires_delta=access_token_expires)

    return Token(access_token=access_token, token_type="bearer")
    

@router.post('/logout')
def logout(token: str = Depends(oauth2_scheme)):
    auth.verify_token(token)
    auth.token_blacklist.add(token)
    return {"message": "Successfully logged out"}