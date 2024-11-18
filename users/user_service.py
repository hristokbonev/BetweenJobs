from sqlmodel import Session, select
from data.db_models import User
from users.user_models import UserRegistrationRequest
from data.db_models import User, Skill, Level
from users.user_models import UsersResponse, UserRegistrationRequest, CreateSkillRequest
from typing import List
from datetime import datetime
import base64


def view_users(session: Session):
    statement = select(User).order_by(User.id)
    users = session.exec(statement).all()

    return users


def view_user_by_id(user_id: int, session: Session):
    statement = select(User.id, User.username, User.first_name, User.last_name, User.is_admin, User.date_of_birth, User.email).where(User.id == user_id)
    user = session.execute(statement).all()

    return user


def create_user(username, password, first_name, last_name, birthdate, email, session: Session):
    # Convert birthdate to an ISO 8601 string format if it's a datetime object
    birthdate_str = birthdate.isoformat() if isinstance(birthdate, datetime) else birthdate

    statement = select(User).where(User.id == user_id)
    user = session.exec(statement).first()

    return user if user else None


# ADMIN Functions
def create_new_skill(data: CreateSkillRequest, session: Session):
    # Check if skill exists
    is_skill = select(Skill).where(Skill.name == data.name)
    existing_skill = session.execute(is_skill).scalars().first()
    if existing_skill:
        raise ValueError(f'Skill {data.skill_name} already exists!')
    # Create new skill record
    new_skill = Skill(**data.model_dump())
    session.add(new_skill)
    session.commit()
    # Return the newly created skill
    find_new_skill = select(Skill).where(Skill.id == new_skill.id)
    response = session.execute(find_new_skill).scalars().first()
    return response

