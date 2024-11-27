import pytest
from sqlmodel import SQLModel, create_engine, Session
from companies.company_models import CreateCompanyRequest, UpdateCompanyRequest
from data.db_models import Company, CompanyUserRole, User, JobAd, Status
from companies import company_service as cs
from datetime import date


# Create a test database using SQLite in memory
@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


# Helper to populate test data
@pytest.fixture
def populate_data(session):
    user1 = User(
        id=1,
        username="user1",
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        password="password",
        is_admin=True,
        date_of_birth=date(1990, 1, 1),
    )
    company1 = Company(
        id=1,
        name="TechCorp",
        description="A tech company",
        author_id=1,
    )
    status1 = Status(
        id=1,
        name="Open"
    )
    job_ad1 = JobAd(
        id=1,
        title="Software Engineer",
        company_id=1,
        company_name="TechCorp",
        status_id=1,  # Provide the required status_id
    )

    session.add(user1)
    session.add(company1)
    session.add(status1)
    session.add(job_ad1)
    session.commit()

# Test: View companies
def test_view_companies(session, populate_data):
    companies = cs.view_companies(session, name="TechCorp")
    assert len(companies) == 1
    assert companies[0].name == "TechCorp"


# Test: View users in a company
def test_view_users_in_company(session, populate_data):
    # Add a user role linking user to the company
    role = CompanyUserRole(company_id=1, user_id=1, role_id=1)
    session.add(role)
    session.commit()

    users = cs.view_users_in_company(comp_id=1, session=session)
    assert len(users) == 1
    assert users[0].username == "user1"


# Test: View company by ID
def test_view_company_by_id(session, populate_data):
    company = cs.view_company_by_id(comp_id=1, session=session)
    assert company is not None
    assert company.name == "TechCorp"


# Test: Create a new company
def test_create_company(session):
    data = CreateCompanyRequest(name="NewCo", description="A new company", author_id=1)
    new_company = cs.create_company(data=data, session=session)

    assert new_company.name == "NewCo"
    assert new_company.description == "A new company"


# Test: Change company details
def test_change_company(session, populate_data):
    update_data = UpdateCompanyRequest(name="UpdatedTechCorp")
    updated_company = cs.change_company(target_id=1, data=update_data, session=session)

    assert updated_company.name == "UpdatedTechCorp"


# Test: Delete company and related data
def test_delete_company(session, populate_data):
    delete_message = cs.delete_company(target_id=1, session=session)

    # Check that the company is deleted
    deleted_company = session.get(Company, 1)
    assert deleted_company is None

    # Verify the delete message
    assert delete_message["message"] == "Company with ID 1 and all related data was deleted!"
