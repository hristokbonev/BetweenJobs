from sqlmodel import Session, select
from data.db_models import User
from users.user_models import UserSearch, UserUpdate
from data.db_models import Skill
from users.user_models import CreateSkillRequest

from utils.auth import get_password_hash


def view_users(session: Session):
    statement = select(User).order_by(User.id)
    users = session.exec(statement).all()

    return users


def view_user_by_id(user_id: int, session: Session):
    statement = select(User).where(User.id == user_id)
    user = session.exec(statement).first()

    return user


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


def update_user(user_id: int, user_update, session: Session):
    stm = select(User).where(User.id == user_id)
    user = session.exec(stm).first()
    
    if not user:
        return None
    
    user.username = user_update.username or user.username

    if user_update.new_password or user_update.confirm_password:
        if user_update.new_password != user_update.confirm_password:
            raise ValueError("New password and confirm password do not match")
        user.password = get_password_hash(user_update.new_password)

    user.first_name = user_update.first_name or user.first_name
    user.last_name = user_update.last_name or user.last_name
    user.email = user_update.email or user.email

  
    session.add(user)
    session.commit()
    session.refresh(user)
  
    return user
