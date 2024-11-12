from sqlmodel import SQLModel, Field



class Education(SQLModel, table=True):
    __tablename__ = "education"

    id : int = Field(primary_key=True, index=True)
    education : str = Field(index=True)