from sqlmodel import Session, select
from data.db_models import User
from users.user_models import UserRegistrationRequest
from datetime import datetime
import base64


def view_users(session: Session):
    statement = select(User).order_by(User.id)
    users = session.execute(statement).scalars().all()

    return users


def view_user_by_id(user_id: int, session: Session):

    statement = select(User).where(User.id == user_id)
    user = session.execute(statement).scalars().first()
    
    return user if user else None


def create_user(user: UserRegistrationRequest, session: Session):
    # Convert birthdate to an ISO 8601 string format if it's a datetime object
    user.date_of_birth = user.date_of_birth.isoformat() if isinstance(user.date_of_birth, datetime) else user.date_of_birth

    # Hash the password securely
    user.password = base64.b64encode(user.password.encode('utf-8')).decode('utf-8')

    new_user = User(
        username=user.username,
        password=user.password,
        first_name=user.first_name,
        last_name=user.last_name,
        date_of_birth=user.date_of_birth,
        email=user.email
    )


    # Add and commit the new user to the session
    session.add(new_user)
    session.commit()

    response = view_user_by_id(new_user.id, session)

    return response if response else None


