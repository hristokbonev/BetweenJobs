from sqlmodel import SQLModel, Field



class EmploymentType(SQLModel, table=True):
    __tablename__ = "employment"

    id : int = Field(primary_key=True, index=True)
    employment : str = Field(index=True)

 