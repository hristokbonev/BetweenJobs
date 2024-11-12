from sqlmodel import SQLModel, Field


class Skills(SQLModel, table=True):
    __tablename__ = "skills"

    id : int = Field(default=None, primary_key=True)
    skill_name : str = Field(default=None, unique=True, index=True)


    