from fastapi import APIRouter, Request, Form, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from data.db_models import User
from users.user_service import get_password_hash, get_user
from utils import auth
from utils.auth import get_current_user, authenticate_user
from utils.authentication import create_user

login_router = APIRouter(prefix='', tags=['Users'])
templates = Jinja2Templates(directory='templates')


@login_router.get('/register', response_model=None)
def serve_register(request: Request):
    return templates.TemplateResponse(name="register.html", request=request)

@login_router.post('/register')
def register(request: Request, username: str = Form(...), password: str = Form(...), confirm_password: str = Form(...), email: str = Form(...), first_name: str = Form(...), last_name: str = Form(...)):
    if get_user(username, password, confirm_password, email, first_name, last_name):
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "error": "User already exists"}
        )
    
    if password != confirm_password:
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "error": "Passwords do not match"}
        )
    
    hashed_password = get_password_hash(password)
    password = hashed_password
    user_data = User(username=username, email=email, first_name=first_name, last_name=last_name, password=hashed_password)
    user_id = create_user(user_data)
    response = RedirectResponse(url=f"/", status_code=302)
    response.set_cookie(key="token", value=auth.create_access_token(data={'sub': username, "id": user_id}))
    return response
        
            

@login_router.get('/login', response_model=None)
def serve_login(request: Request):
    return templates.TemplateResponse(name="login.html", request=request)


@login_router.post('/login')
def login(form_data: OAuth2PasswordRequestForm = Depends(), request: Request = None): 
    user = authenticate_user(form_data.username, form_data.password)  
    if not user:
        return templates.TemplateResponse(
        "login.html",
        {"request": request, "error": "Invalid username or password"}
    )
    
    access_token = auth.create_access_token(data={'sub': user.username, "id": int(user.id)})
    response = RedirectResponse(url="/home.html", status_code=302)
    response.set_cookie(key="token", value=access_token, httponly=True, secure=True)  
    return response



@login_router.get('/home.html', response_model=None)
def serve_login_home(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse(name="home.html", context={"request": request, "user": current_user})


@login_router.post('/home', response_model=None)
def serve_login_home_authenticated(current_user: User = Depends(get_current_user)):
    return {
        "message": "User is authenticated",
        "user": {
            "id": current_user.id,
            "username": current_user.username,
        },
    }

@login_router.get('/logout')
def logout(request: Request = None):
    token = request.cookies.get('token')
    auth.token_blacklist.add(token)
    response = RedirectResponse(url='/', status_code=302)
    response.delete_cookie('token')
    return response

