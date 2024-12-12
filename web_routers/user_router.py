from mailjet_rest import Client
from fastapi import APIRouter, HTTPException, Request, Form, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import false
from sqlmodel import Session, select
from common.template_config import CustomJinja2Templates
from fastapi.responses import RedirectResponse
from data.database import get_session
from data.db_models import User
from users.user_models import UserUpdate
from users.user_service import get_password_hash, update_user
from utils import auth
from utils.auth import authenticate_user
from passlib.context import CryptContext
from datetime import datetime
from itsdangerous import URLSafeTimedSerializer
from common.mailjet_functions import send_email
import os


key_API = os.getenv('key_API')
key_Secret = os.getenv('key_Secret')
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
key = os.getenv("SECRET_KEY")
access_token_expire_minutes = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")


router = APIRouter(prefix='', tags=['Users'])
templates = CustomJinja2Templates(directory='templates')





@router.get('/register', response_model=None)
def serve_register(request: Request):
    return templates.TemplateResponse(name="register.html", request=request)


@router.post('/register')
def register(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    email: str = Form(...),
    first_name: str = Form(...),
    last_name: str = Form(...),
    birth_date: str = Form(...), 
    session: Session = Depends(get_session)
):
    
    if password != confirm_password:
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "error": "Passwords do not match"}
        )

    
    existing_user = session.query(User).filter(User.username == username).first()
    if existing_user:
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "error": "User already exists"}
        )

    try:
        parsed_birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date()
    except ValueError:
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "error": "Invalid date format. Use YYYY-MM-DD."}
        )


    hashed_password = get_password_hash(password)


    new_user = User(
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name,
        password=hashed_password,
        date_of_birth=parsed_birth_date  
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    send_email(
        email=new_user.email,
        name=f"{new_user.first_name or ''} {new_user.last_name or ''}",
        text="Welcome to BetweenJobs",
        subject="Welcome to BetweenJobs",
        html="<h1>Welcome to BetweenJobs</h1>"
    )
  
    token = auth.create_access_token(data={"sub": username, "id": new_user.id})
    response = RedirectResponse(url="/home", status_code=302)
    response.set_cookie(key="token", value=token)
    return response
            

@router.get('/login', response_model=None)
def serve_login(request: Request):
    return templates.TemplateResponse(name="login.html", request=request)


@router.post('/login')
def login(form_data: OAuth2PasswordRequestForm = Depends(), request: Request = None): 
    user = authenticate_user(form_data.username, form_data.password)  
    if not user:
        return templates.TemplateResponse(
        "login.html", context=
        {"request": request, "error": "Invalid username or password"}
    )
    
    access_token = auth.create_access_token(data={'sub': user.username, "user_id": int(user.id)})
    response = RedirectResponse(url="/home", status_code=302)
    response.set_cookie(key="token", value=access_token, httponly=True, secure=True, samesite="Strict")  
    return response


@router.get('/logout')
def logout(request: Request = None):
    token = request.cookies.get('token')
    auth.token_blacklist.add(token)
    response = RedirectResponse(url='/home', status_code=302)
    response.delete_cookie('token')
    return response


@router.get('/reset_password', response_model=None)
def serve_reset_password(request: Request):
    return templates.TemplateResponse(name="reset_password.html", context={"request": request})


@router.post('/reset_password')
def mail(email: str = Form(...)):
  
    serializer = URLSafeTimedSerializer(key)
    token = serializer.dumps({'email': email}, salt='reset-password')
    send_email(email=email, name='', text="Click the link below to reset your password", 
               subject="Reset your password", 
               html=f"<h1>Reset your password</h1><p>Click the link below to reset your password</p><a href='http://localhost:8000/reset_password_form?token={token}'>Reset password</a>")
    
    return RedirectResponse(url='/reset_password', status_code=303)



   
@router.get('/reset_password_form', response_model=None)
def reset_password_form(request: Request):
    return templates.TemplateResponse(name="reset_password_form.html", context={"request": request})


@router.post('/reset_password_form')
def changed_password(request: Request, email: str = Form(...), new_password: str = Form(...), confirm_password: str = Form(...), session: Session = Depends(get_session)):
    if new_password != confirm_password:
        
        return templates.TemplateResponse(
            "reset_password_form.html",
            {"request": request, "error": "Passwords do not match"}
        )
    
    try:
        
        stm = select(User).where(User.email == email)
        user = session.exec(stm).first()

        if not user:
            
            return templates.TemplateResponse(
                "reset_password_form.html",
                {"request": request, "error": "User with this email does not exist."}
            )
        
      
        hashed_password = get_password_hash(new_password)
        user.password = hashed_password

        session.add(user)
        session.commit()

        return templates.TemplateResponse(
            "reset_password_form.html",
            {"request": request, "success": "Your password has been successfully updated."}
        )

    except Exception as e:
    
        print(f"Error updating password: {e}")
        
       
        return templates.TemplateResponse(
            "reset_password_form.html",
            {"request": request, "error": "An error occurred while updating your password. Please try again."}
        )


@router.get('/profile', response_model=None)
def update_profile(request: Request):
    return templates.TemplateResponse(name="profile.html", request=request)

@router.post('/profile')
def post_profile(
    request: Request,
    id: int = Form(...),
    username: str = Form(None),
    first_name: str = Form(None),
    last_name: str = Form(None),
    email: str = Form(None),
    new_password: str = Form(None),
    confirm_password: str = Form(None),
    session: Session = Depends(get_session)
):
    try:
        user_update = UserUpdate(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            new_password=new_password,
            confirm_password=confirm_password
        )
        user = update_user(id, user_update, session)
        if not user:
            return templates.TemplateResponse(
                "profile.html",
                {"request": request, "error": "User not found"}
            )
        return templates.TemplateResponse(
            "profile.html",
            {"request": request, "user": user, "success": "Profile updated successfully"}
        )
    except ValueError as ve:
        return templates.TemplateResponse(
            "profile.html",
            {"request": request, "error": str(ve)}
        )
    except Exception as e:
        return templates.TemplateResponse(
            "profile.html",
            {"request": request, "error": f"An error occurred: {str(e)}"}
        )