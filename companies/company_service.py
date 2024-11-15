from sqlmodel import Session, select

from companies.company_models import CreateCompanyRequest
from data.db_models import Company, CompanyUserRole, User
from users.user_models import UsersResponse


def view_companies(session: Session):
    statement = select(Company)
    companies = session.execute(statement).scalars().all()

    return companies if companies else None


def view_users_in_company(comp_id: int, session: Session):
    user_ids_query = select(CompanyUserRole.user_id).where(CompanyUserRole.company_id == comp_id)
    user_ids = session.execute(user_ids_query).scalars().all()

    if not user_ids:
        return []

    employees_query = select(User).where(User.id.in_(user_ids))
    employees = session.execute(employees_query).scalars().all()
    return [UsersResponse(**dict(row)) for row in employees]


def view_company_by_id(comp_id: int, session: Session):
    statement = select(Company).where(Company.id == comp_id)
    company = session.execute(statement).scalars().first()
    return company


def create_company(data: CreateCompanyRequest, session: Session):
    new_company = Company(**data.model_dump())

    session.add(new_company)
    session.commit()
    new_role = CompanyUserRole()
    response = view_company_by_id(new_company.id, session)
    return response