from sqlalchemy import Column, Integer, String
from sqlmodel import SQLModel, Field


class Statuses(SQLModel, table=True):
    __tablename__ = "statuses"

    id : int = Field(primary_key=True, index=True)
    status_name : str = Field(unique=True, index=True)
    
 