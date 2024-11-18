from data.db_models import Location
from sqlmodel import Session, select


def get_all_locations(session: Session):

    statement = select(Location.name)
    
    locations = session.exec(statement).all()

    return locations if locations else None

def location_exists(location, session: Session):

    statement = select(Location.name).where(Location.name == location)

    location = session.exec(statement).first()

    return bool(location)