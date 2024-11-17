from datetime import datetime, timedelta
import os
from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from data.database import get_db, Session
from starlette import status
from data.db_models import User
# from users.user_service import view_users
# from users.user_models import UsersResponse
from utils.token_models import Token
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt
from utils.token_models import CreateUserRequest


token_router = APIRouter(prefix='/api/token', tags=["Token"])

key = os.getenv("SECRET_KEY")
algorithm = os.getenv("ALGORITHM")
access_token_expire_minutes = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

bcrypto_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/api/token")


db_dependency = Annotated[Session, Depends(get_db)] 


@token_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest)-> User:  # type: ignore

    create_user_model = User(username=create_user_request.username, 
                            password=bcrypto_context.hash(create_user_request.password))
    
    db.add(create_user_model)
    db.commit()
   

@token_router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency): # type: ignore
    user = authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Could not validate user")
    
    # Create the access token with the username and user ID
    token = create_access_token(username=user.username, user_id=user.id, expires_delta=timedelta(minutes=int(access_token_expire_minutes)))
    
    return {"access_token": token, "token_type": "bearer"}


def authenticate_user(db: Session, username: str, password: str) -> User | None: # type: ignore
    user = db.query(User).filter(User.username == username).first()
    if not user or not bcrypto_context.verify(password, user.hashed_password):
        return None
    return user


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': username, 'id':user_id}
    expires = datetime.now() + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, key, algorithm=algorithm)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)], db: Session): # type: ignore
    try:
        payload = jwt.decode(token, key, algorithms=[algorithm])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                detail="Could not validate credentials")
        
        # You should query the database here to get the full user object, including is_admin
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                detail="Could not validate user")
        return user
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Could not validate user")
    

def get_current_admin_user(user: User = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException('You do not have permission to access this')
    return user


  

  