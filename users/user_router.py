from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from users.user_models import UserRegistrationRequest, UsersResponse
from users import user_service as us
from data.database import get_session
from data.db_models import User

users_router = APIRouter(prefix='/api/users', tags=["Users"])

@users_router.get('/')
def show_users(session: Session = Depends(get_session)):
    # try:
    users = us.view_users(session)

    return [UsersResponse.from_query_str(*usr) for usr in users]
    # except ValueError as e:
    #     return HTTPException(status_code=404, detail=str(e))


@users_router.post('/register')
def register_user(new_usr: UserRegistrationRequest, session: Session = Depends(get_session)):
    try:
        return us.create_user(
            new_usr.username,
            new_usr.password,
            new_usr.first_name,
            new_usr.last_name,
            new_usr.date_of_birth,
            new_usr.email,
            session
        )
    except ValueError as e:
        return HTTPException(status_code=404, detail=str(e))

@users_router.get('/users/{user_id}')
def get_user_by_id(user_id: int, session: Session = Depends(get_session)):
    user = us.view_user_by_id(user_id, session)

    if user:
        return (UsersResponse.from_query_str(*usr) for usr in user)