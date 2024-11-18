from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from common.exceptions import NotFoundException
from data.db_models import User
from users.user_models import UserRegistrationRequest, UserSchema, UserSearch, UsersResponse
from users import user_service as us
from data.database import get_session
from typing import List
from users import crud

router = APIRouter(prefix='/api/users', tags=["Users"])

@router.get('/', response_model=List[UsersResponse])
def show_users(session: Session = Depends(get_session)):
    try:
        users = us.view_users(session)

        return users
    except ValueError as e:
        return HTTPException(status_code=404, detail=str(e))


# @router.post('/register', response_model=UsersResponse)
# def register_user(reg_form: UserRegistrationRequest, session: Session = Depends(get_session)):

#     try:
#         return crud.create_user(reg_form=reg_form, session=session)
    
#     except ValueError:
#         return NotFoundException(detail='User could not be created')
    
#     except Exception:
#         return HTTPException(status_code=500, detail='Problem creating user: ')

    
@router.get('/users/{user_id}', response_model=UsersResponse)
def get_user_by_id(user_id: int, session: Session = Depends(get_session)):

    user = us.view_user_by_id(user_id, session)

    return user if user else NotFoundException(detail='User not found')



@router.get("/search", response_model=list[UserSchema])
def search_users( searche_criteria: UserSearch = Depends(),
                 session: Session = Depends(get_session)):
    
    statement = select(User)
    user = session.exec(statement)

    if searche_criteria.username:
        statement = select(User).where(User.username == searche_criteria.username)
        user = session.exec(statement)
    if searche_criteria.first_name:
        statement = select(User).where(User.first_name == searche_criteria.first_name)
        user = session.exec(statement)
    if searche_criteria.last_name:
        statement = select(User).where(User.last_name == searche_criteria.last_name)
        user = session.exec(statement)
    if searche_criteria.email:
        statement = select(User).where(User.email == searche_criteria.email)
        user = session.exec(statement)         

    users = user.all()    

    return users    

