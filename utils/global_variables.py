from typing import List
from sqlmodel import Session, select
from data.db_models import EmploymentType, Education, Location
from utils.variable_models import VariablesResponse


# Global Variables
EMPLOYMENT_TYPES= []
EDUCATION_TYPES = []
LOCATIONS = []

def populate_globals(session: Session,
                     employment: List[str] = None,
                     education: List[str] = None,
                     locations: List[str] = None):
    """
    Populate global variables with distinct values from the database.
    This function populates the settings object with the values fetched from the database.
    """
    # Fetch distinct values for employment types
    employment_types_query = session.exec(select(EmploymentType.name))
    employment = [row for row in employment_types_query]

    # Fetch distinct values for education types
    education_types_query = session.exec(select(Education.degree_level))
    education = [row for row in education_types_query]

    # Fetch distinct values for locations
    locations_query = session.exec(select(Location.name))
    locations = [row for row in locations_query]

    return VariablesResponse(
        EMPLOYMENT_TYPES=employment,
        EDUCATION_TYPES=education,
        LOCATIONS=locations
    )