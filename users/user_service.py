from sqlmodel import Session, select
from data.database import get_session
from data.db_models import User
from users.user_models import UsersResponse
from typing import List
from datetime import datetime
import base64


def view_users(session: Session) -> List[UsersResponse]:
    if session is None:
        session = next(get_session())

    statement = select(User)
    results = session.exec(statement).all()

    all_users = [
        UsersResponse.from_query_str(
            id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            is_admin=user.is_admin,
            date_of_birth=user.date_of_birth,
            email=user.email
        ) for user in results
    ]

    return all_users


def create_user(username, password, first_name, last_name, birthdate, email, session: Session):
    # Convert birthdate to an ISO 8601 string format if it's a datetime object
    birthdate_str = birthdate.isoformat() if isinstance(birthdate, datetime) else birthdate

    # Hash the password securely
    hashed_password = base64.b64encode(password.encode('utf-8')).decode('utf-8')

    # Create a new User instance using the ORM model
    new_user = User(
        username=User.username,
        password=hashed_password,
        first_name=User.first_name,
        last_name=User.last_name,
        date_of_birth=birthdate_str,
        email=User.email
    )

    # Add and commit the new user to the session
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    # Convert the created user to the Pydantic model for response
    created_user = UsersResponse.from_query_str(
        id=new_user.id,
        username=new_user.username,
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        is_admin=new_user.is_admin,
        date_of_birth=new_user.date_of_birth,
        email=new_user.email
    )

    return created_user
