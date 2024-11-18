from sqlmodel import Session, select
from data.db_models import EmploymentType

def employment_type_exists(employment_type, session: Session):
    statement = select(EmploymentType.name).where(EmploymentType.name == employment_type)
    employment_type_name = session.exec(statement).first()

    return bool(employment_type_name)