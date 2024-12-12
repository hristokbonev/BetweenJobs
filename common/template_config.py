from fastapi import Request
from fastapi.templating import Jinja2Templates
from utils.auth import get_current_user
from users.user_service import owns_job_ad, user_has_companies
from data.database import get_session
from data.database import engine
from sqlmodel import Session



class CustomJinja2Templates(Jinja2Templates):
    def __init__(self, directory: str):
        super().__init__(directory=directory)
        self.env.globals['get_user'] = self.get_user_from_request
        self.env.globals['has_company'] = self.user_has_company
        self.env.globals['get_session'] = get_session
        self.env.globals['owns_job_ad'] = self.owns_jobad 

    def get_user_from_request(self, request: Request):
        token = request.cookies.get('token')
        user = get_current_user(token)
        
        if not user:
            return None
        
        return user
    
    def user_has_company(self, user_id: int):
        with Session(engine) as session:
            return user_has_companies(user_id, session=session)
        
    def owns_jobad(self, user_id: int, job_ad_id: int):
        with Session(engine) as session:
            return owns_job_ad(user_id, job_ad_id, session=session)