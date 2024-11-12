from sqlmodel import SQLModel, Field




class Matches(SQLModel, table=True):
    __tablename__ = "matches"

    resume_id : int = Field(foreign_key="resumes.id", primary_key=True)
    job_id : int = Field(foreign_key="jobs.id", primary_key=True)

  