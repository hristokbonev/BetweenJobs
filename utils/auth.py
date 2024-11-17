from datetime import datetime, timedelta
import os
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from data.database import get_db, Session
from starlette import status
# from ..users.user_service import view_users
# from BetweenJobs.users.user_models import UsersResponse
from utils.token_models import Token, Users
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
async def create_user(db: db_dependency, create_user_request: CreateUserRequest): # type: ignore
    create_user_model = Users(username=create_user_request.username, 
                              hashed_password=bcrypto_context.hash(create_user_request.password),
    )
    
    db.add(create_user_model)
    db.commit()
    return create_user_model

@token_router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                  db: db_dependency): # type: ignore
    user = autenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Could not validate user")
    token = create_access_token(user.username, user.id, timedelta(minutes=int(access_token_expire_minutes)))
    
    return {"access_token": token, "token_type": "bearer"}

def autenticate_user(db: Session, username: str, password: str): # type: ignore
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        raise False
    if not bcrypto_context.verify(password, user.hashed_password):
       False
    return user


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': username, 'id':user_id}
    expires = datetime.now() + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, key, algorithm=algorithm)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payloade = jwt.decode(token, key, algorithms=[algorithm])
        username: str = payloade.get("sub")
        user_id: int = payloade.get("id")
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                detail="Could not validate credentials")
        return {"username": username, "id": user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Could not validate user")
    
def get_current_admin_user(user: Users = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException('You do not have permission to access this')
    return user
      

# @token_router.get("/", response_model=list[UsersResponse])
# async def get_all_users(admin: Users = Depends(get_current_admin_user)):
#     return user_service.view_users()

   
  