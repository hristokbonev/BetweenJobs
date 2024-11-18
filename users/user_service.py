import logging
from sqlmodel import Session, select
from data.db_models import User
from users.user_models import UserRegistrationRequest, UserSearch, UserUpdate



from utils.auth import get_password_hash


def view_users(session: Session):
    statement = select(User).order_by(User.id)
    users = session.exec(statement).all()

    return users


def view_user_by_id(user_id: int, session: Session):

    statement = select(User).where(User.id == user_id)
    user = session.exec(statement).first()

    return user if user else None


def get_filtered_users(search_criteria: UserSearch, page: int, limit: int, session: Session):
    statement = select(User)

    if search_criteria.username:
        statement = statement.filter(User.username.ilike(f"%{search_criteria.username}%"))
    if search_criteria.first_name:
        statement = statement.filter(User.first_name.ilike(f"%{search_criteria.first_name}%"))
    if search_criteria.last_name:
        statement = statement.filter(User.last_name.ilike(f"%{search_criteria.last_name}%"))
    if search_criteria.email:
        statement = statement.filter(User.email.ilike(f"%{search_criteria.email}%"))

    offset = (page - 1) * limit
    statement = statement.offset(offset).limit(limit)

    users = session.exec(statement).all()

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
   

#    