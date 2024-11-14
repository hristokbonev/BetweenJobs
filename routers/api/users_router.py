from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from data.models.user import User
from data.database import get_session

router = APIRouter()

@router.get("/users/")
def get_users(db: Session = Depends(get_session)):
    return db.query(User).all()