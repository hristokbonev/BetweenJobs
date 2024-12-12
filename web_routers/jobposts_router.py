from fastapi import APIRouter, Request, Depends, Query, Form, Response
from data.database import get_session
from sqlmodel import Session
from jobposts.jobpost_models import CreateJobAdRequest
from utils import auth as au
from jobposts import jobpost_service as js
from utils import attribute_service as ats
from companies import company_service as cs
from common.template_config import CustomJinja2Templates
from datetime import timedelta


jobs_router = APIRouter(prefix='/jobposts')
jobs_edit_router = APIRouter()
templates = CustomJinja2Templates(directory='templates')


@jobs_router.get('/')
def default_view(
    request: Request, 
    session: Session = Depends(get_session),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100)
):
    job_adds = js.show_all_posts(session=session)

    all_jobs = len(job_adds)
    # Apply pagination
    start = (page -1) * limit
    end = start + limit
    paginated_jobs = job_adds[start:end]
    total_pages = (all_jobs + limit - 1) // limit

    # Get locations and employment tyepes for dropdown list
    locations = list(ats.get_all_locations(session))
    employments = list(ats.get_all_employments(session))
    # Map company logo by company ID
    logos = ats.get_all_logos(session)
    logo_dict = {company.company_id: company.logo_url for company in logos if company.logo_url}
    print(logo_dict)
    token = request.cookies.get('token')
    context={
        'request': request, 
        'jobadds': paginated_jobs,
        'alladds': all_jobs,
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
    else:
        return templates.TemplateResponse(
            request=request,
            name='login.html', 
            context=context
        ) 

    return templates.TemplateResponse(
        request=request,
        name='job-listings.html', 
        context=context
    )

# Utility function for rendering search resuls in search()
def _get_search_data(
    keyword: str = Form(...),
    search_field: str = Form(...),
    region: str = Form(...),
    job_type: str = Form(...)
):
    return keyword, search_field, region, job_type


@jobs_router.post('/')
def search(
    request: Request, 
    session: Session = Depends(get_session),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    form_data = Depends(_get_search_data)
):
    # Obtain filtered elements
    print(form_data)
    keyword, search_field, region, jobtype = form_data
    # Map search_field to function arguments
    filter_args = {}
    if search_field and keyword:
        filter_args[search_field] = keyword
    if region:
        filter_args["location.name"] = region
    if jobtype:
        filter_args['employment.name'] = jobtype
    # Get job posts and sum of jobposts
    job_adds = js.show_all_posts(
        session=session,
        **filter_args
    )

    all_jobs = len(job_adds)
    # Apply pagination
    start = (page -1) * limit
    end = start + limit
    paginated_jobs = job_adds[start:end]
    total_pages = (all_jobs + limit - 1) // limit

    # Get locations and employment tyepes for dropdown list
    locations = list(ats.get_all_locations(session))
    employments = list(ats.get_all_employments(session))
    # Map company logo by company ID
    logos = ats.get_all_logos(session)
    logo_dict = {company.company_id: company.logo_url for company in logos if company.logo_url}

    token = request.cookies.get('token')
    context={
        'request': request, 
        'jobadds': paginated_jobs,
        'alladds': all_jobs,
        'current_page': page,
        'total_pages': total_pages,
        'min': min,
        'filters': {
            'search_field': search_field,
            'keyword': keyword
        },
        'locations': locations,
        'employments': employments,
        'filters': filter_args,
        'logo_dict': logo_dict
    }

    if token:
        user = au.get_current_user(token)
        context['user'] = user

    return templates.TemplateResponse(
        request=request,
        name='job-listings.html', 
        context=context
    )


@jobs_router.get('/create')
def display_create_view(
    request: Request, 
    session: Session = Depends(get_session)
):
    # Get locations and employment tyepes for dropdown list
    locations = list(ats.get_all_locations(session))
    employments = list(ats.get_all_employments(session))
    educations = list(ats.get_all_educations(session))
    skills = ats.get_all_skills(session)


    token = request.cookies.get('token')
    context={
        'locations': locations, 
        'employments': employments,
        'educations': educations,
        'skills': skills
    }

    if token:
        user = au.get_current_user(token)
        context['user'] = user

        companies = cs.get_companies_by_owner_id(user.id, session)
        context['companies'] = companies

    
    return templates.TemplateResponse(
        request=request,
        name='post-job.html', 
        context=context
    )
    


@jobs_router.get('/{id}')
def show_jobpost(
    id: int,
    request: Request,
    session: Session = Depends(get_session)
):

    target_job = js.view_job_post_by_id(id, session)

    deadline = target_job.created_at + timedelta(days=30)
    location = ats.get_location_by_id(target_job.location_id, session)
    employment = ats.get_employment_type_by_id(target_job.employment_type_id, session)
    logo = ats.get_company_logo(target_job.company_id, session)

    # Get required skills for the job post
    skills = ats.get_skills_for_job(target_job.id, session)

    token = request.cookies.get('token')
    context={
        'request': request, 
        'jobad': target_job,
        'min': min,
        'location': location,
        'employment': employment,
        'skills': skills,
        'deadline': deadline,
        'logo': logo
    }

    if token:
        user = au.get_current_user(token)
        context['user'] = user
    else:
        return templates.TemplateResponse(
            request=request,
            name='login.html', 
            context=context
        ) 
    

    return templates.TemplateResponse(
        request=request,
        name='job-single.html', 
        context=context
    )


# Utility function for collecting inputs for CREATE JOBPOST
def _get_crete_data(
    title: str = Form(...),
    company: int = Form(...),
    description: str = Form(...),
    education: int = Form(...),
    employment: int = Form(...),
    location: int = Form(...),
    salary: float = Form(...),
    skills: list[int] = Form(...)
):
    return title, company, description, education, employment, location, salary, skills


@jobs_router.post('/create')
def create_new_job_post(
    request: Request, 
    session: Session = Depends(get_session),
    form_data = Depends(_get_crete_data)
):
    # Obtain form inputs and dump them in JobPost Create model
    title, company, description, education, employment, location, salary, skills = form_data

    skills = [int(skill) for skill in skills]
    company_name = cs.view_company_by_id(comp_id=company, session=session)
    
    job_post_data = CreateJobAdRequest(
        title=title,
        company_id=company,
        company_name=company_name.name,
        description=description,
        education_id=education,
        salary=salary,
        employment_type_id=employment,
        location_id=location,
        skill_ids=skills
    )

    # Create new Job object
    new_company = js.create_job_post(data=job_post_data, session=session)
    # Get additional data for the context
    logo = ats.get_company_logo(new_company.company_id, session)
    deadline = new_company.created_at + timedelta(days=30)
    token = request.cookies.get('token')
    context={
        'request': request, 
        'jobad': new_company,
        'min': min,
        'location': location,
        'employment': employment,
        'skills': skills,
        'deadline': deadline,
        'logo': logo
    }

    if token:
        user = au.get_current_user(token)
        context['user'] = user
    
    return show_jobpost(id=new_company.id, request=request, session=session)
