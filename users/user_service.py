from aiohttp.abc import HTTPException
from sqlmodel import Session, select
from data.db_models import User, Skill, Level
from users.user_models import UsersResponse, UserRegistrationRequest, CreateSkillRequest
from typing import List
from datetime import datetime
import base64


def view_users(session: Session):
    statement = select(User)
    users = session.execute(statement).scalars().all()

    return users if users else None


def view_user_by_id(user_id: int, session: Session):
    statement = select(User).where(User.id == user_id)
    user = session.execute(statement).scalars().first()

    return user if user else None


def create_user(data: UserRegistrationRequest, session: Session):
    # Convert birthdate to an ISO 8601 string format if it's a datetime object
    birthdate_str = data.birthdate.isoformat() if isinstance(data.birthdate, datetime) else data.birthdate

    # Hash the password securely
    hashed_password = base64.b64encode(data.password.encode('utf-8')).decode('utf-8')

    # Create a new User instance using the ORM model
    new_user = User(**data.model_dump())

    # Add and commit the new user to the session
    session.add(new_user)
    session.commit()

    response = view_user_by_id(new_user.id, session)
    return response


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

