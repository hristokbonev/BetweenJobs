from sqlmodel import Session, select
from data.db_models import Status

def status_exists(status, session: Session):
    statement = select(Status.name).where(Status.name == status)
    status_type = session.exec(statement).first()

    return bool(status_type)