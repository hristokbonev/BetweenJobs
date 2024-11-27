from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from common.exceptions import UnauthorizedException
from data.database import get_session
from matches import match_service as ms
from matches.match_models import MatchResponse
from users.user_models import UserModel
from utils.auth import get_current_user


match_router = APIRouter(prefix='/api/match', tags=['Match'])


@match_router.post('/', response_model=MatchResponse)
def match_resume_with_job_ad(resume_id: int, job_id: int, session: Session = Depends(get_session), current_user: UserModel = Depends(get_current_user)):
    print(current_user)
    if not current_user:
        raise UnauthorizedException(detail='You need to be authenticated to use this service')
    try:
        match_data = ms.match_with_job_ad(resume_id, job_id, session)
        if not match_data:
            HTTPException(status_code=500, detail=f"Failed to match resume with job ad. Please select valid item.")
        return match_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")
