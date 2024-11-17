from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from sqlmodel import Session
from data.db_models import User
from users.user_models import UsersResponse
from utils.auth import authenticate_user, create_access_token, get_current_user
from utils.token_models import Token
from data.database import get_db, get_session
from users import user_service as us

token_router = APIRouter(prefix='/api/token', tags=["Token"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/token/login")


@token_router.post("/login", response_model=Token)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    """Authenticate user and issue JWT token."""
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create JWT access token
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}



@token_router.post("/", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@token_router.get('/me', response_model=UsersResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user

