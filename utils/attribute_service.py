from sqlmodel import Session, select
from data.db_models import Education, EmploymentType, Location, Skill, Status


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


def education_exists(education, session: Session):
    statement = select(Education.id).where(Education.degree_level == education)
    education_type = session.exec(statement).first()

    return bool(education_type)


def employment_type_exists(employment_type, session: Session):
    statement = select(EmploymentType.name).where(EmploymentType.name == employment_type)
    employment_type_name = session.exec(statement).first()
    return bool(employment_type_name)


def get_all_locations(session: Session):
    statement = select(Location.name)
    locations = session.exec(statement).all()
    return locations if locations else None


def location_exists(location, session: Session):
    statement = select(Location.name).where(Location.name == location)
    location = session.exec(statement).first()
    return bool(location)


def skill_exists(skill, session: Session):
    statement = select(Skill.name).where(Skill.name == skill)
    skill = session.exec(statement).first()
    return bool(skill)


def status_exists(status, session: Session):
    statement = select(Status.name).where(Status.name == status)
    status_type = session.exec(statement).first()
    return bool(status_type)