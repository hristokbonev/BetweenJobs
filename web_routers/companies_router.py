from fastapi import APIRouter, HTTPException, Request, Depends, Query, Form, Response
from data.database import get_session
from sqlmodel import Session
from common.template_config import CustomJinja2Templates
from users.user_models import UserModel
from utils import auth as au
from companies import company_service as cs
from utils import attribute_service as ats
from jobposts import jobpost_service as js
from companies.company_service import get_companies_by_owner_id, view_company_by_id


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


@company_router.get('/my_companies')
def my_companies(request: Request, session: Session = Depends(get_session)):
    token = request.cookies.get('token')
    user = au.get_current_user(token)
    companies = get_companies_by_owner_id(user.id, session)
    all_companies = len(companies)
    context = {
        'request': request,
        'companies': companies,
        'all_companies': all_companies
    }
    return templates.TemplateResponse(
        request=request,
        name='my_companies.html',
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
    jobs = js.view_jobs_by_company_id_with_id_included(comp_id=target_company.id, session=session)

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


# @router.get('/{id}')
# def view_company(request: Request, id: int, session: Session = Depends(get_session)):
#     token = request.cookies.get('token')
#     user = au.get_current_user(token)
#     if not user:
#         return templates.TemplateResponse(
#             request=request,
#             name='login.html',
#             context={}
#         )
#     company = view_company_by_id(comp_id=id, session=session)
#     if not company:
#         return templates.TemplateResponse(
#             request=request,
#             name='404.html',
#             context={}
#         )
#     context = {
#         'request': request,
#         'company': company
#     }
#     return templates.TemplateResponse(
#         request=request,
#         name='company-single.html',


@company_router.get('/create', response_class=None)
def create_company(request: Request):
    return templates.TemplateResponse(
        name='reg_company.html',
        context={'request': request}    
    )

@company_router.get('/edit/{id}', response_class=None)
def edit_company(request: Request, id: int, session: Session = Depends(get_session)):
    company = view_company_by_id(id, session)
    location = ats.get_location_by_id(company.id, session)
    logo = ats.get_company_logo(company.id, session)
    skills = ats.get_skills_for_job(company.id, session)
    token = request.cookies.get('token')
    context = {
        'request': request,
        'company': company,
        'min': min,
        'location': location,
        'logo': logo,
        'skills': skills
    }

    if token:
        user = au.get_current_user(token)
        context['user'] = user

    return templates.TemplateResponse(
        name='company-single.html',
        context=context
    )

@company_router.post('/create')   
def create_company_form(
    request: Request,
    name: str = Form(...),
    industry: str = Form(...),
    location: str = Form(...),
    description: str = Form(...),
    email: str = Form(...),
    phone_number: str = Form(...),
    company_website: str = Form(None),
    session: Session = Depends(get_session)
):
    token = request.cookies.get('token')
    user = au.get_current_user(token)
    if not user:
        return templates.TemplateResponse(
            request=request,
            name='login.html',
            context={}
        )
    
    # Validate form data
    if not name or not industry or not location or not description or not email or not phone_number:
        return templates.TemplateResponse(
            request=request,
            name='reg_company.html',
            context={'request': request, 'error': 'All fields are required.'}
        )
    
    company = cs.create_company(
        name=name,
        industry=industry,
        location=location,
        description=description,
        email=email,
        phone_number=phone_number,
        company_website=company_website,
        owner_id=user.id,  # Ensure owner_id is set correctly
        session=session
    )
    return templates.TemplateResponse(
        request=request,
        name='company-single.html',
        context={'company': company}
    )