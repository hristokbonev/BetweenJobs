from fastapi import APIRouter, Request, Depends, Query, Form, Response
from data.database import get_session
from sqlmodel import Session
from common.template_config import CustomJinja2Templates
from utils import auth as au
from companies import company_service as cs
from utils import attribute_service as ats
from jobposts import jobpost_service as js


company_router = APIRouter(prefix='/companies')
templates = CustomJinja2Templates(directory='templates')


@company_router.get('/')
def default_view(
    request: Request, 
    session: Session = Depends(get_session),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100)
):
    companies = cs.view_companies(session)
    all_companies = len(companies)

    # Apply pagination
    start = (page -1) * limit
    end = start + limit
    paginated_companies = companies[start:end]
    total_pages = (all_companies + limit - 1) // limit

    # Get locations and employment tyepes for dropdown list
    locations = list(ats.get_all_locations(session))
    employments = list(ats.get_all_employments(session))
    # Map company logo by company ID
    logos = ats.get_all_logos(session)
    logo_dict = {company.company_id: company.logo_url for company in logos if company.logo_url}
    token = request.cookies.get('token')
    context={
        'request': request, 
        'companies': paginated_companies,
        'allcompanies': all_companies,
        'current_page': page,
        'total_pages': total_pages,
        'min': min, 
        'filters': {
            'search_field': None,
            'keyword': None
        },
        'locations': locations,
        'employments': employments,
        'logo_dict': logo_dict
    }

    if token:
        user = au.get_current_user(token)
        context['user'] = user

    return templates.TemplateResponse(
        request=request,
        name='company-listings.html', 
        context=context
    )


@company_router.get('/{id}')
def show_jobpost(
    id: int,
    request: Request,
    session: Session = Depends(get_session)
):
    target_company = cs.view_company_by_id(id, session)
    logo = ats.get_company_logo(id, session)
    jobs = js.view_jobs_by_company_id(id, session)

    token = request.cookies.get('token')
    context={
        'request': request, 
        'company': target_company,
        'jobs': jobs,
        'min': min,
        'logo': logo
    }

    if token:
        user = au.get_current_user(token)
        context['user'] = user

    return templates.TemplateResponse(
        request=request,
        name='company-single.html', 
        context=context
    )