from fastapi import Request
from fastapi.templating import Jinja2Templates
from utils.auth import get_current_user
from users.user_service import user_has_companies


class CustomJinja2Templates(Jinja2Templates):
    def __init__(self, directory: str):
        super().__init__(directory=directory)
        self.env.globals['get_user'] = self.get_user_from_request
        self.env.globals['has_company'] = self.user_has_company

    def get_user_from_request(self, request: Request):
        token = request.cookies.get('token')
        user = get_current_user(token)
        
        if not user:
            return None
        
        return user
    
    def user_has_company(self, user_id: int):
        return user_has_companies(user_id)