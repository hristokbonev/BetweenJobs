from sqlmodel import Session, select
from data.database import get_session, engine
from data.db_models import User
from users.user_models import UsersResponse
from typing import List
from datetime import datetime
import base64


def view_users(session: Session):
    statement = select(User.id, User.username, User.first_name, User.last_name, User.is_admin, User.date_of_birth, User.email)
    users = session.execute(statement).all()

    return users


def view_user_by_id(user_id: int, session: Session):
    statement = select(User.id, User.username, User.first_name, User.last_name, User.is_admin, User.date_of_birth, User.email).where(User.id == user_id)
    user = session.execute(statement).all()

    return user


def create_user(username, password, first_name, last_name, birthdate, email, session: Session):
    # Convert birthdate to an ISO 8601 string format if it's a datetime object
    birthdate_str = birthdate.isoformat() if isinstance(birthdate, datetime) else birthdate

    # Hash the password securely
    hashed_password = base64.b64encode(password.encode('utf-8')).decode('utf-8')

    # Create a new User instance using the ORM model
    new_user = User(
        username=username,
        password=hashed_password,
        first_name=first_name,
        last_name=last_name,
        is_admin=False,
        date_of_birth=birthdate_str,
        email=email
    )

    # Add and commit the new user to the session
    session.add(new_user)
    session.commit()

    response = view_user_by_id(new_user.id, session)
    return response


