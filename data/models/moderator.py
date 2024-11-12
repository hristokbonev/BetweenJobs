from sqlmodel import SQLModel, Field



class Moderators(SQLModel, table=True):
    __tablename__ = "moderators"

    company_id : int = Field(foreign_key="companies.id", primary_key=True)
    user_id : int = Field(foreign_key="users.id", primary_key=True)
    role_id : int = Field(foreign_key="roles.id", primary_key=True)

