from sqlalchemy.orm import Session
from data.db_models import Skill
from sqlmodel import select


def skill_exists(skill, session: Session):

    statement = select(Skill.name).where(Skill.name == skill)

    skill = session.exec(statement).first()

    return bool(skill)