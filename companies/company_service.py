from fastapi import HTTPException
from sqlmodel import Session, select
from typing import Optional
from companies.company_models import CreateCompanyRequest, UpdateCompanyRequest
from data.db_models import Company, CompanyUserRole, User, JobAd
from users.user_models import UsersResponse


def view_companies(session: Session, name: Optional[str] = None, job_ad_title: Optional[str] = None):
    statement = select(Company).join(JobAd, isouter=True).distinct(Company.id)

    if name and job_ad_title:
        # Explicit join and filter for both conditions
        statement = (
            select(Company)
            .join(JobAd, Company.id == JobAd.company_id)
            .filter(Company.name.ilike(f"%{name}%"), JobAd.title.ilike(f"%{job_ad_title}%"))
            .distinct(Company.id)
        )
    elif name:
        # Filter only on company name
        statement = statement.filter(Company.name.ilike(f'%{name}%')).distinct(Company.id)
    elif job_ad_title:
        # Explicit join and filter on job_ad_title only
        statement = (
            select(Company)
            .join(JobAd, Company.id == JobAd.company_id)
            .where(JobAd.title.ilike(f"%{job_ad_title}%"))
            .distinct(Company.id)
        )

    companies = session.exec(statement).all()

    return [Company(**dict(row)) for row in companies]


def view_users_in_company(comp_id: int, session: Session):
    user_ids_query = select(CompanyUserRole.user_id).where(CompanyUserRole.company_id == comp_id)
    user_ids = session.exec(user_ids_query).all()

    if not user_ids:
        return []

    employees_query = select(User).where(User.id.in_(user_ids))
    employees = session.exec(employees_query).all()
    return [UsersResponse(**dict(row)) for row in employees]


def view_company_by_id(comp_id: int, session: Session):
    statement = select(Company).where(Company.id == comp_id)
    company = session.exec(statement).first()
    return company


def create_company(data: CreateCompanyRequest, session: Session):
    # Insert new company data
    new_company = Company(**data.model_dump())
    session.add(new_company)
    session.commit()
    # Insert new user role relation with new company id
    new_role = CompanyUserRole(
        company_id=new_company.id,
        user_id=new_company.author_id,
        role_id=1  # Assuming 1 is the ID for the desired role
    )
    session.add(new_role)
    session.commit()
    # display response to client
    response = view_company_by_id(new_company.id, session)
    return response


def change_company(target_id: int, data: UpdateCompanyRequest, session: Session):
    statement = select(Company).where(Company.id == target_id)
    target_company = session.exec(statement).first()
    if not target_company:
        raise HTTPException(status_code=404, detail="Company not found.")

    if data.name:
        target_company.name = data.name
    if data.description:
        target_company.description = data.description
    if data.author_id:
        target_company.author_id = data.author_id

    session.commit()

    return target_company


def delete_company(target_id: int, session: Session):
    # Find the company record and delete it
    statement = select(Company).where(Company.id == target_id)
    target_company = session.exec(statement).first()
    if not target_company:
        raise HTTPException(status_code=404, detail="Company not found.")

    # Find related company roles and delete them all
    query_roles = select(CompanyUserRole).where(CompanyUserRole.company_id == target_id)
    related_roles = session.exec(query_roles).all()
    for role in related_roles:
        session.delete(role)
        session.commit()

    # Find related job ads for the company and delete them all
    query_jobs = select(JobAd).where(JobAd.company_id == target_id)
    related_jobs = session.exec(query_jobs).all()
    for job in related_jobs:
        session.delete(job)
        session.commit()

    session.delete(target_company)

    session.commit()
    return {"message": f"Company with ID {target_id} and all related data was deleted!"}


def get_companies_by_owner_id(user_id: int, session: Session):
    statement = select(Company).join(User, Company.author_id == User.id).where(User.id == user_id)
    companies = session.exec(statement).all()
    return companies

