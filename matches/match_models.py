from pydantic import BaseModel


class MatchResponse(BaseModel):
    user_id: int
    user_full_name: str
    user_profession: str
    job_position: str
    company_id: int
    company_name: str
    match_score: float


class JobFeedback(BaseModel):
    job_id: int
    accepted: bool
    resume_id: int