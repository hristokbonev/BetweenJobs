from datetime import timedelta
import os
from fastapi import APIRouter, Depends, HTTPException, status
from itsdangerous import URLSafeTimedSerializer
from data.db_models import User
from users.user_service import update_user
from utils import auth
from users.user_models import UserCreate, UserSchema, Token, UserUpdate
from utils.auth import  create_access_token, get_password_hash
from data.database import engine, create_db
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session, select
from common.mailjet_functions import send_email
from passlib.context import CryptContext


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
    send_email(email=db_user.email, name=(db_user.first_name or '')+ ' ' + (db_user.last_name or ''), text= "Welcome to BetweenJobs", subject= "Welcome to BetweenJobs", html= "<h1>Welcome to BetweenJobs</h1>")
    return db_user


@router.put('/{user_id}', response_model=UserSchema )
def update_user_info(user_id: int, user_update: UserUpdate = Depends(), session: Session = Depends(get_session)):

    updated_user = update_user(user_id, user_update, session)
    
    if not updated_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return updated_user
    

@router.post('/login', response_model=Token)
def login(from_data: OAuth2PasswordRequestForm = Depends()):
    user = auth.authenticate_user(from_data.username, from_data.password)
    
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


@router.post('/reset_password_request')
def reset_password_request(email: str, session: Session = Depends(get_session)):
    stm = select(User).where(User.email == email)
    user = session.exec(stm).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    serializer = URLSafeTimedSerializer(key)
    token = serializer.dumps({'user_id': user.id}, salt="password-reset-salt")
    
    # send_reset_password_email(user.email, token)
    send_email(email=user.email, name=(user.first_name or '')+ ' ' + (user.last_name or ''), text= "Reset your password", 
               subject= "Reset your password", 
               html= f"""
                    <h1>Reset your password</h1>
                    <p>Click the link below to reset your password</p>
                    <a href='http://127.0.0.1:8000/docs#/Users/reset_password_direct_api_users_reset_password_direct_post'>Reset Password</a>
                    """)
    return {"message": "Password reset email sent. Check your inbox."}



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



@router.post('/reset_password_direct')
def reset_password_direct(email: str,  new_password: str, confirm_password: str, session: Session = Depends(get_session)):
    """
    Update the user's password after validating the current password.
    """
    # Ensure the new password and confirm password match
    if new_password != confirm_password:
        raise HTTPException(status_code=400, detail="New passwords do not match")
    
    # Find the user by email
    stm = select(User).where(User.email == email)
    user = session.exec(stm).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    
    # Hash and update the new password
    user.password = pwd_context.hash(new_password)
    session.add(user)
    session.commit()
    
    return {"message": "Password successfully updated"}


