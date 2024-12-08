from fastapi import APIRouter, Request, Depends, Query, Form
from starlette.templating import Jinja2Templates
from data.database import get_session
from sqlmodel import Session
from utils import auth as au
from matches import match_service as ms


match_router = APIRouter(prefix='/match')
templates = Jinja2Templates(directory='templates')


@match_router.post('/match')
def match_job_w_resume(
    request: Request, 
    session: Session = Depends(get_session)
):
    # Retrieve job_id and user_id from cookies
    job_id = request.cookies.get('job_id')
    resume_id = request.cookies.get('resume_id')

    print('JOb ID: ', job_id, ' Resume ID: ', resume_id)
    match_data = ms.match_with_job_ad(resume_id, job_id, session)
    token = request.cookies.get('token')
    
    context={
        'request': request, 
        'match': match_data
    }

    if token:
        user = au.get_current_user(token)
        context['user'] = user

    return templates.TemplateResponse(
        request=request,
        name='match.html', 
        context=context
    )