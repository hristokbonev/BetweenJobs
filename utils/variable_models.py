from typing import List
from pydantic import BaseModel


class VariablesResponse(BaseModel):
    EMPLOYMENT_TYPES: List[str] = []
    EDUCATION_TYPES: List[str] = []
    LOCATIONS: List[str] = []