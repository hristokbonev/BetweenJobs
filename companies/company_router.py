from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from companies.company_models import CompanyResponse, CreateCompanyRequest, UpdateCompanyRequest
from data.database import get_session
from companies import company_service as cs
from jobposts import jobpost_service as js
from users.user_models import UserModel
from utils.auth import get_current_user
from common import exceptions as ex
from typing import List, Optional, Dict


companies_router = APIRouter(prefix='/api/companies', tags=["Companies"])

@companies_router.get('/', response_model=List[CompanyResponse])
def show_all_companies(
    name: Optional[str] = None,
    job_ad_title: Optional[str] = None,
    session: Session = Depends(get_session),
    current_user: UserModel = Depends(get_current_user)
):
    if not current_user:
        raise ex.UnauthorizedException(detail='You must be logged in to view resumes')
    try:
        companies = cs.view_companies(session, name=name, job_ad_title=job_ad_title)
        if not companies:
            raise HTTPException(status_code=404, detail="No companies found.")

        return companies

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")


@companies_router.get('/{comp_id}', response_model=CompanyResponse)
def show_company_by_id(comp_id: int, session: Session = Depends(get_session), current_user: UserModel = Depends(get_current_user)):
    if not current_user:
        raise ex.UnauthorizedException(detail='You must be logged in to view resumes')
    try:
        company = cs.view_company_by_id(comp_id, session)
        if not company:
            raise HTTPException(status_code=404, detail=f"Company with ID {comp_id} not found.")
        employees = cs.view_users_in_company(comp_id, session)
        job_ads = js.view_jobs_by_company_id(comp_id, session)

        return CompanyResponse(
            name=company.name,
            description=company.description,
            author_id=company.author_id,
            employees=employees,
            job_ads=job_ads
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")


@companies_router.post('/', response_model=CompanyResponse)
def register_new_company(data: CreateCompanyRequest, session: Session = Depends(get_session), current_user: UserModel = Depends(get_current_user)):
    if not current_user:
        raise ex.UnauthorizedException(detail='You must be logged in to view resumes')
    try:
        new_company = cs.create_company(data, session)
        if not new_company:
            raise HTTPException(status_code=500, detail=f"Failed to create company with name {data.company_name}.")
        return new_company
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")


@companies_router.put('/{comp_id}', response_model=CompanyResponse)
def modify_company_by_id(
        comp_id: int,
        data: UpdateCompanyRequest,
        session: Session = Depends(get_session),
        current_user: UserModel = Depends(get_current_user)):
    if not current_user:
        raise ex.UnauthorizedException(detail='You must be logged in to view resumes')
    try:
        updated_company = cs.change_company(session=session, target_id=comp_id, data=data)
        return updated_company
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Server error: {str(e)}')


@companies_router.delete('/{comp_id}', response_model=Dict[str, str])
def delete_company_by_id(company_id: int, session: Session = Depends(get_session), current_user: UserModel = Depends(get_current_user)):
    if not current_user:
        raise ex.UnauthorizedException(detail='You must be logged in to view resumes')
    return cs.delete_company(target_id=company_id, session=session)