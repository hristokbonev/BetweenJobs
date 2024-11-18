from sqlmodel import Session, select
from data.db_models import Education

def education_exists(education, session: Session):
    statement = select(Education.id).where(Education.degree_level == education)
    education_type = session.exec(statement).first()

    return bool(education_type)