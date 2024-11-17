from data.database import get_session, Session
from fastapi import APIRouter, Depends, HTTPException
from resumes.resume_models import ResumeResponse
from common.exceptions import NotFoundException
from resumes import resume_services as rs
from typing import List  

router = APIRouter(prefix='/api/resumes', tags=['Resumes'])

@router.get('/', response_model=List[ResumeResponse] | ResumeResponse) 
def view_resumes(session: Session = Depends(get_session)):

    resumes = rs.get_all_resumes(session)

    return resumes if resumes else NotFoundException(detail='No resumes found')

@router.get('/{id}', response_model=ResumeResponse)
def view_resume(id: int, session: Session = Depends(get_session)):

    resume = rs.get_resume_by_id(id, session)

    return resume if resume else NotFoundException(detail='Resume not found')

