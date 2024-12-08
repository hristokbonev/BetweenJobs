# from datetime import datetime, timedelta
# from multiprocessing.connection import Client
# import os
# from django.http import HttpResponseRedirect
# from fastapi import APIRouter, Request, Form, Depends
# from fastapi.security import OAuth2PasswordRequestForm
# from fastapi.templating import Jinja2Templates
# from fastapi.responses import RedirectResponse
# from itsdangerous import URLSafeTimedSerializer
# from sqlmodel import Session, select
# from common.mailjet_functions import send_email
# from data.database import get_session
# from data.db_models import User
# from tests.conftest import session
# from users.user_models import Token
# from users.user_service import get_password_hash, get_user
# from utils import auth
# from utils.auth import get_current_user, authenticate_user
# from utils.authentication import create_user
# from passlib.context import CryptContext


# key_API = os.getenv('key_API')
# key_Secret = os.getenv('key_Secret')
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# key = os.getenv("SECRET_KEY")
# access_token_expire_minutes = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

# login_router = APIRouter(prefix='', tags=['Users'])
# templates = Jinja2Templates(directory='templates')




# @login_router.post('/register')
# def register(request: Request,
#     username: str = Form(...),
#     password: str = Form(...),
#     confirm_password: str = Form(...),
#     email: str = Form(...),
#     first_name: str = Form(...),
#     last_name: str = Form(...),
#     birth_date: str = Form(...)
#     ):
    
#     if get_user(username=username, password=password, email=email):
#         return templates.TemplateResponse(
#             "register.html",
#             {"request": request, "error": "User already exists"}
#         )
    
#     if password != confirm_password:
#         return templates.TemplateResponse(
#             "register.html",
#             {"request": request, "error": "Passwords do not match"}
#         )
    
#     hashed_password = get_password_hash(password)
#     password = hashed_password
#     user_data = User(username=username, email=email, first_name=first_name, last_name=last_name, password=hashed_password, date_of_birth=birth_date)
#     user_id = create_user(user_data)
#     send_email(
#         email=user_data.email, 
#         name=(user_data.first_name or '') + ' ' + (user_data.last_name or ''), 
#         text="Welcome to BetweenJobs", 
#         subject="Welcome to BetweenJobs", 
#         html="<h1>Welcome to BetweenJobs</h1>"
#     )
#     response = RedirectResponse(url=f"/", status_code=302)
#     response.set_cookie(key="token", value=auth.create_access_token(data={'sub': username, "id": user_id}))
#     return response
        
            








    # email = request.form['email']
    # mailjet = Client(auth=(key_API, key_Secret), version='v3.1')
    # data = {
    #     'Messages': [
    #         {
    #             "From": {
    #                 "Name": "BetweenJobs",
    #                 "Email": "betweenjobsplatform@gmail.com",
    #             },
    #             "To": [
    #                 {
    #                     "Email": email,
    #                     "Name": "",
    #                 }
    #             ],
    #             "TemplateID": 6541657,
    #             "TemplateLanguage": True,
    #             "Subject": "check",
    #             "Variables": {
    #                 "firstname": ""
    #             }
    #         }
    #     ]
    # }
    # result = mailjet.send.create(data=data)
    # return HttpResponseRedirect('/')