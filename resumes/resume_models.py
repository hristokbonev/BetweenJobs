from pydantic import BaseModel

class ResumeResponse(BaseModel):

    user_id: int
    username: str
    full_name: str | None = None
    title: str
    education: str | None = None
    job_description: str | None = None
    status: str
    employment_type: str | None = None
    location: str | None = None
    id: int

    class Config:
        orm_mode = True


class ResumeRequest(BaseModel):

    user_id: int
    full_name: str | None = None
    title: str
    education: str | None = None
    job_description: str | None = None
    status: str
    employment_type: str | None = None
    location: str | None = None
    id: int | None = None
    skills: list[str] | None = None

    class Config:
        orm_mode = True