from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from common.exceptions import NotFoundException
from data.db_models import User
from users.user_models import UserRegistrationRequest, UserSchema, UserSearch, UsersResponse, CreateSkillRequest
from users import user_service as us
from data.database import get_session
from typing import List

router = APIRouter(prefix='/api/users', tags=["Users"])

@router.get('/', response_model=List[UsersResponse])
def show_users(session: Session = Depends(get_session)):
    try:
        users = us.view_users(session)

        return users
    except ValueError as e:
        return HTTPException(status_code=404, detail=str(e))

    
@router.get('/users/{user_id}', response_model=UsersResponse)
def get_user_by_id(user_id: int, session: Session = Depends(get_session)):

    user = us.view_user_by_id(user_id, session)

    return user if user else NotFoundException(detail='User not found')



@router.get("/search", response_model=List[UserSchema])
def search_users(search_criteria: UserSearch = Depends(), 
                 page: int = 1, 
                 limit: int = 10, 
                 session: Session = Depends(get_session)):

    users = us.get_filtered_users(search_criteria, page, limit, session)
    return users 


# Admin controls
@router.post('/admin/skill')
def register_new_skill(data: CreateSkillRequest, session: Session = Depends(get_session)):
    try:
        new_skill = us.create_new_skill(data=data, session=session)
        if not new_skill:
            raise HTTPException(status_code=406, detail="This skill already exists!")
        return new_skill
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")
