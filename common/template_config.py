from fastapi import Request
from fastapi.templating import Jinja2Templates
from utils.auth import get_current_user


class CustomTemplates(Jinja2Templates):
    def __init__(self, directory: str):
        super().__init__(directory=directory)
        self.env.globals['get_user'] = self.get_user_from_request

    def get_user_from_request(self, request: Request):
        token = request.cookies.get('token')
        user = get_current_user(token)
        
        if not token or user:
            return None
        
        return user
    

   