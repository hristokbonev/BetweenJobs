from sqlmodel import Session, select
from data.db_models import User
from users.user_models import UserRegistrationRequest
from datetime import datetime
import base64


def view_users(session: Session):
    statement = select(User).order_by(User.id)
    users = session.exec(statement).all()

    return users


def view_user_by_id(user_id: int, session: Session):

    statement = select(User).where(User.id == user_id)
    user = session.exec(statement).first()

    return user if user else None
