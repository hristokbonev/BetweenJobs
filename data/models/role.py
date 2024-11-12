from sqlmodel import SQLModel, Field



class Roles(SQLModel, table=True):
    __tablename__ = "roles"

    id : int = Field(primary_key=True, index=True)
    role_name : str = Field(unique=True, index=True)

