from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from common.exceptions import NotFoundException
from users.user_models import UserRegistrationRequest, UsersResponse
from users import user_service as us
from data.database import get_session
from typing import List

router = APIRouter(prefix='/api/users', tags=["Users"])

@router.get('/', response_model=List[UsersResponse])
def show_users(session: Session = Depends(get_session)):
    # try:
    users = us.view_users(session)

    return users
    # except ValueError as e:
    #     return HTTPException(status_code=404, detail=str(e))


@router.post('/register', response_model=UsersResponse)
def register_user(new_usr: UserRegistrationRequest, session: Session = Depends(get_session)):

    try:
        return us.create_user(new_usr, session)
    
    except ValueError:
        return NotFoundException(detail='User could not be created')
    
    except Exception:
        return HTTPException(status_code=500, detail='Problem creating user: ')

    
@router.get('/users/{user_id}', response_model=UsersResponse)
def get_user_by_id(user_id: int, session: Session = Depends(get_session)):

    user = us.view_user_by_id(user_id, session)

    return user if user else NotFoundException(detail='User not found')