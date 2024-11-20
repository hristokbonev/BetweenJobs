from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from common.exceptions import NotFoundException, UnauthorizedException
from data.db_models import User
from users.user_models import CreateSkillRequest, UserSchema, UserSearch, UserUpdate, UsersResponse, UserModel
from users import user_service as us
from data.database import get_session
from typing import List

from utils.auth import get_current_user, get_password_hash


router = APIRouter(prefix='/api/users', tags=["Users"])

@router.get('/', response_model=List[UsersResponse])
def show_users(session: Session = Depends(get_session), current_user: UserModel = Depends(get_current_user)):

    if not current_user:
        raise UnauthorizedException(detail='You must be logged in to view users')

    users = us.view_users(session)

    if not users:
        raise NotFoundException(detail='No users found')

    return users
    
    
@router.get('/users/{user_id}', response_model=UsersResponse)
def get_user_by_id(user_id: int, session: Session = Depends(get_session), current_user: UserModel = Depends(get_current_user)):

    if not current_user:
        raise UnauthorizedException(detail='You must be logged in to view users')

    user = us.view_user_by_id(user_id, session)

    if not user:
        raise NotFoundException(detail='User not found')
    
    return user


@router.get("/search", response_model=List[UserSchema])
def search_users(search_criteria: UserSearch = Depends(), 
                 page: int = 1, 
                 limit: int = 10, 
                 session: Session = Depends(get_session), current_user: UserModel = Depends(get_current_user)):
    
    if not current_user:
        raise UnauthorizedException(detail='You must be logged in to view users')

    users = us.get_filtered_users(search_criteria, page, limit, session)

    if not users:
        raise NotFoundException(detail='No users found')
    
    return users 


def update_user(user_id: int, user_update: UserUpdate, session: Session):
    stm = select(User).where(User.id == user_id)
    user = session.exec(stm).first()
    
    if not user:
        return None

    if user_update.username is not None:
        user.username = user_update.username
    if user_update.password is not None:
        user.password = get_password_hash(user_update.password) 
    if user_update.first_name is not None:
        user.first_name = user_update.first_name
    if user_update.last_name is not None:
        user.last_name = user_update.last_name
    if user_update.email is not None:
        user.email = user_update.email

    session.add(user)
    session.commit()

    return user




# Admin controls
@router.post('/admin/skill')
def register_new_skill(data: CreateSkillRequest, session: Session = Depends(get_session), current_user: UserModel = Depends(get_current_user)):

    if not current_user:
        raise UnauthorizedException(detail='You must be an admin to create a new skill')
    
    if not current_user.is_admin:
        raise UnauthorizedException(detail='You must be an admin to create a new skill')
    
    try:
        new_skill = us.create_new_skill(data=data, session=session)
        if not new_skill:
            raise HTTPException(status_code=406, detail="This skill already exists!")
        return new_skill
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")
