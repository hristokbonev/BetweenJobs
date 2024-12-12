from fastapi import APIRouter, Request, Depends, Form
from data.database import get_session
from sqlmodel import Session
from utils import attribute_service as ats
from utils import auth as au
from users import user_service as us
from jobposts import jobpost_service as js
from resumes import resume_services as rs
from companies import company_service as cs
from common.template_config import CustomJinja2Templates

router = APIRouter(prefix='')
templates = CustomJinja2Templates(directory='templates')


@router.get('/')
def index(request: Request):
    return templates.TemplateResponse(request=request, name='index.html')
    

@router.get('/home')
def serve_home(request: Request, session: Session = Depends(get_session)):
    locations = list(ats.get_all_locations(session))
    employments = list(ats.get_all_employments(session))
    users = len(us.view_users(session))
    jobs = len(js.show_all_posts(session))
    resumes = len(rs.show_all_resumes(session))
    companies = len(cs.view_companies(session))

    token = request.cookies.get('token')
    context={
        'request': request, 
        'locations': locations,
        'employments': employments,
        'filters': {
            'search_field': None,
            'keyword': None
        },
        'all_users': users,
        'all_jobs': jobs,
        'all_resumes': resumes,
        'all_companies': companies
    }

    if token:
        user = au.get_current_user(token)
        context['user'] = user

    return templates.TemplateResponse(
        request=request,
        name='home.html', 
        context=context
    )
        
