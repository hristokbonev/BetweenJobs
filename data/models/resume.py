from sqlmodel import SQLModel, Field



class Resumes(SQLModel, table=True):
    __tablename__ = "resumes"

    user_id : int = Field(foreign_key="users.id", primary_key=True)
    username : str = Field(index=True)
    full_name : str = Field(index=True)
    title : str = Field(index=True)
    education : str = Field(index=True)
    job_description : str = Field(index=True)
    skills_id : int = Field(foreign_key="skills.id")
    location : str = Field(index=True)
    status : str = Field(index=True)
    employment_id : int = Field(foreign_key="employment.id")
    employment : str = Field(index=True)
    id : int = Field(primary_key=True, index=True)

