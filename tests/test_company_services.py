import pytest
from sqlmodel import select
from companies.company_models import CreateCompanyRequest, UpdateCompanyRequest
from companies import company_service as cs
from data.db_models import Company, CompanyUserRole, User, JobAd


@pytest.mark.usefixtures("session")
class TestCompany:
    def test_view_companies(self, session):
        # Arrange
        company1 = Company(id=1, name="Tech Corp", description="Tech Company", author_id=10)
        company2 = Company(id=2, name="Health Inc", description="Healthcare", author_id=10)
        job1 = JobAd(id=1, title="Engineer", company_id=1, company_name='TestCorp')
        job2 = JobAd(id=2, title="Nurse", company_id=2, company_name='TestLTD')

        session.add_all([company1, company2, job1, job2])
        session.commit()

        # Act
        results = cs.view_companies(session, name="Tech", job_ad_title="Engineer")

        # Assert
        assert len(results) == 1
        assert results[0].name == "Tech Corp"

    def test_view_users_in_company(self, session):
        # Arrange
        user1 = User(id=1, username="alice", email="alice@example.com")
        user2 = User(id=2, username="bob", email="bob@example.com")
        company_user_role = CompanyUserRole(company_id=1, user_id=1, role_id=2)
        session.add_all([user1, user2, company_user_role])
        session.commit()

        # Act
        results = cs.view_users_in_company(1, session)

        # Assert
        assert len(results) == 1
        assert results[0].username == "alice"

    def test_view_company_by_id(self, session):
        # Arrange
        company = Company(id=1, name="Tech Corp", description="Tech Company")
        session.add(company)
        session.commit()

        # Act
        result = cs.view_company_by_id(1, session)

        # Assert
        assert result.name == "Tech Corp"

    def test_create_company(self, session):
        # Arrange
        data = CreateCompanyRequest(name="New Co", description="New Company", author_id=1)

        # Act
        result = cs.create_company(data, session)

        # Assert
        assert result.name == "New Co"
        assert result.description == "New Company"

    def test_change_company(self, session):
        # Arrange
        company = Company(id=1, name="Old Co", description="Old Description")
        session.add(company)
        session.commit()
        update_data = UpdateCompanyRequest(name="Updated Co", description="Updated Description")

        # Act
        result = cs.change_company(1, update_data, session)

        # Assert
        assert result.name == "Updated Co"
        assert result.description == "Updated Description"

    def test_delete_company(self, session):
        # Arrange
        company = Company(id=1, name="Delete Me")
        job = JobAd(id=1, title="Job", company_id=1)
        role = CompanyUserRole(company_id=1, user_id=1, role_id=1)
        session.add_all([company, job, role])
        session.commit()

        # Act
        result = cs.delete_company(1, session)

        # Assert
        assert result["message"] == "Company with ID 1 and all related data was deleted!"
        assert session.exec(select(Company).where(Company.id == 1)).first() is None
