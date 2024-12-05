import pytest
from fastapi import HTTPException
from sqlmodel import SQLModel, create_engine, Session
from data.db_models import (
    JobAd, Education, Location, EmploymentType, Status, User, Company
)
from jobposts import jobpost_service as jps
from datetime import date

from jobposts.jobpost_models import CreateJobAdRequest, UpdateJobAdRequest


# Create a test database using SQLite in memory
@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


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
    education1 = Education(id=1, degree_level="Bachelor's")
    location1 = Location(id=1, name="Remote")
    employment1 = EmploymentType(id=1, name="Part-Time")
    employment2 = EmploymentType(id=2, name="Full-Time")
    status1 = Status(id=1, name="Open")
    status2 = Status(id=2, name="Hidden")
    job_ad1 = JobAd(
        id=1,
        title="Software Engineer",
        company_name="TechCorp",
        description="Develop software",
        salary=80000,
        education_id=1,
        location_id=1,
        employment_type_id=1,
        status_id=1,
        company_id=1,
    )
    job_ad2 = JobAd(
        id=2,
        title="Software Engineer",
        company_name="TechCorp",
        description="Develop software",
        salary=80000,
        education_id=1,
        location_id=1,
        employment_type_id=1,
        status_id=2,
        company_id=1,
    )
    job_ad3 = JobAd(
        id=3,
        title="Software Engineer",
        company_name="TechCorp",
        description="Develop software",
        salary=80000,
        education_id=1,
        location_id=1,
        employment_type_id=2,
        status_id=1,
        company_id=1,
    )

    session.add_all([user1, company1, education1, location1, employment1, employment2, status1, status2, job_ad1, job_ad2, job_ad3])
    session.commit()


# Test: show_all_posts
def test_show_all_posts(session, populate_data):
    results = jps.show_all_posts(
        session=session,
        page=1,
        limit=10
    )
    assert len(results) == 3


# Test: view_job_post_by_id
def test_view_job_post_by_id(session, populate_data):
    result = jps.view_job_post_by_id(ad_id=1, session=session)
    assert result.title == "Software Engineer"
    assert result.location == "Remote"
    assert result.employment == "Part-Time"
    assert result.education == "Bachelor's"


# Test: create_job_post
def test_create_job_post(session, populate_data):
    data = CreateJobAdRequest(
        title="Data Analyst",
        company_name="DataCorp",
        description="Analyze data",
        salary=70000,
        education_id=1,
        location_id=1,
        employment_type_id=1,
        status_id=1,
        company_id=1,
        skill_ids=[],
        skill_levels=[],
    )
    response = jps.create_job_post(data=data, session=session)
    assert response.title == "Data Analyst"
    assert response.company_name == "DataCorp"


# Test: change_job_post
def test_change_job_post(session, populate_data):
    data = UpdateJobAdRequest(description="Analyze and interpret data")
    result = jps.change_job_post(target_id=1, data=data, session=session)
    assert result.description == "Analyze and interpret data"


# Test: view_jobs_by_company_id
def test_view_jobs_by_company_id(session, populate_data):
    results = jps.view_jobs_by_company_id(comp_id=1, session=session)
    assert len(results) == 1
    assert results[0].company_name == "TechCorp"


# Test: show_posts_with_names_not_id
def test_show_posts_with_names_not_id(session, populate_data):
    results = jps.show_posts_with_names_not_id(session=session)
    assert len(results) == 1
    assert results[0].title == "Software Engineer"
    assert results[0].skills == []