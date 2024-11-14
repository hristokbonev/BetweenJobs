from fastapi import APIRouter
from data.models.models import User
from sqlmodel import Session, select
from data.database import get_session
from fastapi import Depends

router = APIRouter()

# Endpoint to get a user and their companies
@router.get("/users/{user_id}")
def get_user_companies(user_id: int, session: Session = Depends(get_session)):
    statement = select(User).where(User.id == user_id)
    user = session.exec(statement).first()
    
    if user:
        return {"user": user}
   