from pydantic import BaseModel

class ResumeResponse(BaseModel):

    id: int
    user_id: int
    full_name: str
    
    description: str
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True