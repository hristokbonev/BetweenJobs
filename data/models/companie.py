from sqlmodel import SQLModel, Field
from sqlalchemy import TIMESTAMP


class Companies(SQLModel, table=True):
    __tablename__ = "companies"

    id : int = Field(default=None, primary_key=True)
    created_at : str = TIMESTAMP
    company_name : str = Field(index=True)
    description : str = Field(index=True)
    employees : int = Field(index=True)
    author_id : int = Field(foreign_key="users.id")

    
