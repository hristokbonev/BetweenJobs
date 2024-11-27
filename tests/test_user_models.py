from unittest.mock import MagicMock
from datetime import datetime
from data.db_models import User
from users.user_models import UserModel, UsersResponse

def mock_user(id: int, username: str, email: str, first_name: str, 
                last_name: str, created_at: datetime, is_admin: bool,
                date_of_birth: datetime, employer_id: int, password: str):
        
    user = MagicMock(spec=User)
    user.id = id
    user.username = username
    user.email = email
    user.first_name = first_name
    user.last_name = last_name
    user.created_at = created_at
    user.is_admin = is_admin
    user.date_of_birth = date_of_birth
    user.employer_id = employer_id
    user.password = password

    return user

def mock_user_model(id: int, username: str, email: str, first_name: str, 
                last_name: str, created_at: datetime, is_admin: bool,
                date_of_birth: datetime, employer_id: int, password: str):
        
    user = MagicMock(spec=UserModel)
    user.id = id
    user.username = username
    user.email = email
    user.first_name = first_name
    user.last_name = last_name
    user.is_admin = is_admin
    user.date_of_birth = date_of_birth

    return user
