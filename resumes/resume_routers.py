from data.database import get_session
from sqlmodel import Session
from fastapi import APIRouter, Depends, HTTPException, Query
from resumes.resume_models import ResumeRequest, ResumeResponse, ResumeUpdate
from common.exceptions import NotFoundException
from resumes import resume_services as rs
from typing import List, Optional, Union
from typing import Literal
from locations import location_services as ls

router = APIRouter(prefix='/api/resumes', tags=['Resumes'])

@router.get('/', response_model=Union[List[ResumeResponse], ResumeResponse]) 
def view_resumes(session: Session = Depends(get_session), 
                 name: Optional[str] = Query(None),
                 location: Optional[str] = Query(None),
                 employment_type: Optional[Literal['Full-time', 'Part-time', 'Contract', 'Temporary', 'Internship', 'Volunteer']] = Query(None),
                 education: Optional[Literal['High School', 'Undergraduate degree', 'Postgraduate degree', 'PhD', 'Diploma']] = Query(None),
                 status: Optional[Literal['Active', 'Hidden', 'Private', 'Matched', 'Archived', 'Busy']] = Query(None),
                 title: Optional[str] = Query(None),
                 skills: Optional[List[str]] = Query(None)):

    resumes = rs.get_all_resumes(session=session, name=name, location=location, employment_type=employment_type, education=education, status=status, title=title, skills=skills)

    return resumes if resumes else NotFoundException(detail='No resumes found')

@router.get('/{id}', response_model=ResumeResponse)
def view_resume(id: int, session: Session = Depends(get_session)):

    resume = rs.get_resume_by_id(id, session)

    return resume if resume else NotFoundException(detail='Resume not found')


@router.post('/create', response_model=ResumeResponse)
def create_resume(resume_form: ResumeRequest, session: Session = Depends(get_session)):

    resume = rs.create_resume(resume_form, session)

    return resume if resume else NotFoundException(detail='Resume could not be created')


@router.put('/update/{id}', response_model=ResumeResponse)
def update_resume(id: int, resume_form: ResumeUpdate, session: Session = Depends(get_session)):

    resume = rs.update_resume(id, resume_form, session)

    return resume if resume else NotFoundException(detail='Resume could not be updated')

@router.delete('/delete/{id}', response_model=None)

def delete_resume(id: int, session: Session = Depends(get_session)):
    
    resume = rs.delete_resume(id, session)

    return resume if resume else NotFoundException(detail='Resume could not be deleted')