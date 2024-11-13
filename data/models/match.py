from sqlmodel import SQLModel, Field


class Match(SQLModel, table=True):
    __tablename__ = "Matches"

    resume_id: int = Field(foreign_key="Resumes.id", primary_key=True)
    jobad_id: int = Field(foreign_key="JobAds.id", primary_key=True)
