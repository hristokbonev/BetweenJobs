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


def create_user(reg_form: UserRegistrationRequest, session: Session):
    # Convert birthdate to an ISO 8601 string format if it's a datetime object
    reg_form.date_of_birth = reg_form.date_of_birth.isoformat() if isinstance(reg_form.date_of_birth, datetime) else reg_form.date_of_birth

    # Hash the password securely
    reg_form.password = base64.b64encode(reg_form.password.encode('utf-8')).decode('utf-8')

    # Create a new User object (SQLModel model) from the UserRegistrationRequest object (Pydantic model)
    new_user = User(**reg_form.model_dump())

    # Add and commit the new user to the session
    session.add(new_user)
    session.commit()

    response = view_user_by_id(new_user.id, session)

    return response if response else None


