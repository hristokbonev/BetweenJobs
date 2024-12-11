from fastapi import APIRouter, Request, Depends, Response
from starlette import status
from fastapi.responses import RedirectResponse
from data.database import get_session
from sqlmodel import Session
from resumes.resume_models import ResumeRequest
from utils import auth as au
from resumes import resume_services as rs
from common.template_config import CustomJinja2Templates
from utils.attribute_service import get_all_locations, get_all_employments, get_all_educations, get_all_statuses
from resumes.resume_services import resume_create_form



router = APIRouter(prefix='/resumes')
templates = CustomJinja2Templates(directory='templates')


@router.get('/create')
def show_create_resume(request: Request, session: Session = Depends(get_session)):
    locations = get_all_locations(session)
    employments = get_all_employments(session)
    educations = get_all_educations(session)
    statuses = get_all_statuses(session)

    return templates.TemplateResponse(
        request=request,
        name='create-resume.html',
        context={'request': request, 'locations': locations, 'employments': employments,
                 'educations': educations, 'statuses': statuses})

@router.post('/create')
def create_resume(request: Request, resume: ResumeRequest = Depends(resume_create_form), session: Session = Depends(get_session)):
    token = request.cookies.get('token')
    user = au.get_current_user(token)
    if not user:
        return RedirectResponse(url='/login')
    rs.create_resume(resume_form=resume, session=session, user=user)
    return RedirectResponse(url='/resumes/my_resumes', status_code=status.HTTP_302_FOUND)


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
    if not user:
        return RedirectResponse(url='/login')
    resume = rs.get_resume_by_id(id=id, session=session)
    return templates.TemplateResponse(
        request=request,
        name='portfolio-single.html',
        context={'resume': resume}
    )

