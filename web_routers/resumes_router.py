from fastapi import APIRouter, Request, Depends, Query, Form, Response
from starlette.templating import Jinja2Templates
from data.database import get_session
from sqlmodel import Session
from utils import auth as au
from resumes import resume_services as rs
from common.template_config import CustomJinja2Templates


router = APIRouter(prefix='/resumes')
templates = CustomJinja2Templates(directory='templates')

@router.get('/my_resumes')
def my_resumes(request: Request, session: Session = Depends(get_session)):
    token = request.cookies.get('token')
    user = au.get_current_user(token)
    resumes = rs.get_resumes_by_user_id(user_id=user.id, session=session)
    all_resumes = len(resumes)
    context = {
        'request': request,
        'resumes': resumes,
        'all_resumes': all_resumes
    }
    return templates.TemplateResponse(
        request=request,
        name='resumes.html',
        context=context
    )

@router.get('/{id}')
def view_resume(request: Request, id: int, session: Session = Depends(get_session)):
    token = request.cookies.get('token')
    user = au.get_current_user(token)
    resume = rs.get_resume_by_id(id=id, session=session)
    if resume.user_id != user.id:
        return Response(status_code=403)
    context = {
        'request': request,
        'resume': resume
    }
    return templates.TemplateResponse(
        request=request,
        name='portfolio-single.html',
        context=context
    )