from sqlmodel import Session, select
from data.db_models import Education, EmploymentType, Location


def view_education_by_id(education_id: int, session: Session):
    statement = select(Education.degree_level).where(Education.id == education_id)
    education = session.execute(statement).scalars().first()
    return education


def get_employment_by_id(employment_id: int, session: Session):
    statement = select(EmploymentType.name).where(EmploymentType.id == employment_id)
    employment = session.execute(statement).scalars().first()
    return employment


def get_location_by_id(location_id: int, session: Session):
    statement = select(Location.name).where(Location.id == location_id)
    location = session.execute(statement).scalars().first()
    return location

# Used to dynamically call column values for dynamic reference
# Used for Education, EmploymentType, Skills, Location
def get_distinct_column_values(session: Session, column):
    statement = select(column).distinct()
    results = session.exec(statement).all()
    return [value for value, in results if value]