from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from users.user_models import UserRegistrationRequest, UsersResponse, CreateSkillRequest
from users import user_service as us
from data.database import get_session
from typing import List

users_router = APIRouter(prefix='/api/users', tags=["Users"])

@users_router.get('/', response_model=List[UsersResponse])
def show_users(session: Session = Depends(get_session)):
    try:
        users = us.view_users(session)
        if not users:
            raise HTTPException(status_code=404, detail="No users found.")
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")


@users_router.post('/register', response_model=UsersResponse)
def register_user(new_usr: UserRegistrationRequest, session: Session = Depends(get_session)):
    try:
        user = us.create_user(new_usr, session)
        if not user:
            raise HTTPException(status_code=500, detail="Failed to create user.")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")


@users_router.get('/users/{user_id}', response_model=UsersResponse)
def get_user_by_id(user_id: int, session: Session = Depends(get_session)):
    try:
        user = us.view_user_by_id(user_id, session)
        if not user:
            raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found.")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")


# Admin controls
@users_router.post('/admin/skill')
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
