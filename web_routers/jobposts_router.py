from fastapi import APIRouter, Request, Depends, Query
from starlette.templating import Jinja2Templates
from data.database import get_session
from sqlmodel import Session
from utils import auth as au
from jobposts import jobpost_service as js


jobs_router = APIRouter(prefix='/jobposts')
templates = Jinja2Templates(directory='templates')


@jobs_router.get('/')
def default(
    request: Request, 
    session: Session = Depends(get_session),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100)
):
    # Get job posts and sum of jobposts
    job_adds = js.show_all_posts(session)
    all_jobs = len(job_adds)
    # Apply pagination
    start = (page -1) * limit
    end = start + limit
    paginated_jobs = job_adds[start:end]
    total_pages = (all_jobs + limit - 1) // limit

    token = request.cookies.get('token')
    context={
        'request': request, 
        'jobadds': paginated_jobs,
        'alladds': all_jobs,
        'current_page': page,
        'total_pages': total_pages,
        'min': min
    }

    if token:
        user = au.get_current_user(token)
        context['user'] = user

    return templates.TemplateResponse(
        request=request,
        name='job-listings.html', 
        context=context
    )