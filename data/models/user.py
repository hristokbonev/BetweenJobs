from datetime import datetime
from pydantic import BaseModel


class Users(BaseModel):
    __tablename__ = "users"

    id: int | None = None
    # created_at: Optional[datetime] = Field(default_factory=datetime.now)
    username : str
    # password : str = Field()
    first_name : str
    last_name : str
    is_admin : bool
    date_of_birth : datetime
    email : str

    # job_ads: Relationship = Relationship(back_populates="users")
    # resumes: Relationship = Relationship(back_populates="users")

    @classmethod
    def from_query_str(cls, id, username, first_name, last_name, is_admin, date_of_birth, email):
        return cls(
            id=id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            is_admin=is_admin,
            date_of_birth=date_of_birth,
            email=email
        )
    
class UserRegistrationRequest(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str
    date_of_birth: datetime
    email: str



