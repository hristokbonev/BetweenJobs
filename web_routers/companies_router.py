from fastapi import APIRouter, Request, Depends
from data.database import get_session
from sqlmodel import Session
from utils import auth as au
from common.template_config import CustomJinja2Templates
from companies.company_service import get_companies_by_owner_id, view_company_by_id



templates = CustomJinja2Templates(directory='templates')
router = APIRouter(prefix='/companies')

@router.get('/my_companies')
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

@router.get('/{id}')
def view_company(request: Request, id: int, session: Session = Depends(get_session)):
    token = request.cookies.get('token')
    user = au.get_current_user(token)
    if not user:
        return templates.TemplateResponse(
            request=request,
            name='login.html',
            context={}
        )
    company = view_company_by_id(comp_id=id, session=session)
    if not company:
        return templates.TemplateResponse(
            request=request,
            name='404.html',
            context={}
        )
    context = {
        'request': request,
        'company': company
    }
    return templates.TemplateResponse(
        request=request,
        name='company-single.html',
        context=context
    )