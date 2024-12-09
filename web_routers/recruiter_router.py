from fastapi import APIRouter, Request, Depends, Query, Form, Response
from data.database import get_session
from sqlmodel import Session
from utils import auth as au
from resumes import resume_services as rs
from matches import suggest_service as ss
from common.template_config import CustomJinja2Templates

templates = CustomJinja2Templates(directory='templates')
router = APIRouter(prefix='/recruiter')

@router.get('/resume/{id}')
def recruit(request: Request, id: int, session: Session = Depends(get_session)):
    token = request.cookies.get('token')
    user = au.get_current_user(token)
    resume = rs.get_resume_by_id(id=id, session=session)
    matches = ss.suggest_job_ads(resume_id=id, session=session)
    if resume.user_id != user.id:
        return Response(status_code=403)
    context = {
        'resume': resume,
        'matches': matches
    }
    return templates.TemplateResponse(
        request=request,
        name='recruiter.html',
        context=context
    )