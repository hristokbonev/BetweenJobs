from unittest import TestCase
from datetime import datetime
from pydantic import ValidationError
from sqlmodel import Session, SQLModel, create_engine
from resumes import resume_services as rs
from data.db_models import User, Location, Education, Status, EmploymentType, Skill
from fastapi.testclient import TestClient
from main import app
from resumes.resume_models import ResumeRequest, ResumeResponse

client = TestClient(app)

class TestResumeModels(TestCase):

    def setUp(self):
        self.testuser = User(id=1, username='testuser', email='testuser@email.com',
                                        first_name='Test', last_name='User', created_at=datetime.strptime('2021-01-01', '%Y-%m-%d'),
                                        is_admin=False, date_of_birth=datetime.strptime('1990-01-01', '%Y-%m-%d'), employer_id=None, password='password')
        
        self.testlocattion = Location(id=1, name='Sofia')
        self.testlocation2 = Location(id=2, name='Plovdiv')

        self.testeducation = Education(id=1, degree_level='Undergraduate degree')
        self.testeducation2 = Education(id=2, degree_level='High school')

        self.teststatus = Status(id=1, name='Active')
        self.teststatus2 = Status(id=2, name='Inactive')

        self.testemploymenttype = EmploymentType(id=1, name='Full-time')
        self.testemploymenttype2 = EmploymentType(id=2, name='Part-time')

        self.testskill = Skill(id=1, name='Python')
        self.testskill2 = Skill(id=2, name='Java')
        self.testskill3 = Skill(id=3, name='MySQL')


        self.engine = create_engine("sqlite:///testing.db", connect_args={"check_same_thread": False})

        SQLModel.metadata.drop_all(self.engine)
        SQLModel.metadata.create_all(self.engine)

        self.session = Session(self.engine)

        with self.session.begin():
                self.session.add_all([
                    self.testuser, self.testlocattion, self.testlocation2, self.testeducation, self.testeducation2,
                    self.teststatus, self.teststatus2, self.testemploymenttype, self.testemploymenttype2,
                    self.testskill, self.testskill2, self.testskill3
                ])

                self.session.commit()
            

    def get_session_override(self):

        with Session(self.engine) as session:
            return session
        

    def testCreateResume_CreatesResume(self):

        resume_form = ResumeRequest(full_name='Test User', title='Software Engineer', education='Undergraduate degree', summary='Summary of resume', status='Active', employment_type='Full-time', location='Sofia', skills=['Python', 'Java', 'MySQL'])


        resume = rs.create_resume(user=self.testuser, resume_form=resume_form, session=self.session)


        expected = ResumeResponse(id=1, user_id=1, full_name='Test User', title='Software Engineer', summary='Summary of resume',
                                  username='testuser', employment_type='Full-time', education='Undergraduate degree', location='Sofia',
                                  status='Active', skills=['Python', 'Java', 'MySQL'])

        self.assertEqual(resume, expected)


    def testCreateResume_InvalidEducation_RaiseValidationError(self):


        with self.assertRaises(ValidationError):
            ResumeRequest(full_name='Test User', title='Software Engineer', education='Invalid education', summary='Summary of resume', status='Active', employment_type='Full-time', location='Sofia', skills=['Python', 'Java', 'MySQL'])
    

    def testCreateResume_InvalidStatus_RaiseValidationError(self):


        with self.assertRaises(ValidationError):
            ResumeRequest(full_name='Test User', title='Software Engineer', education='Undergraduate degree', summary='Summary of resume', status='Invalid status', employment_type='Full-time', location='Sofia', skills=['Python', 'Java', 'MySQL'])


    def testCreateResume_InvalidEmploymentType_RaiseValidationError(self):


        with self.assertRaises(ValidationError):
            ResumeRequest(full_name='Test User', title='Software Engineer', education='Undergraduate degree', summary='Summary of resume', status='Active', employment_type='Invalid employment type', location='Sofia', skills=['Python', 'Java', 'MySQL'])


    def testCreateResume_InvalidLocation_RaiseValidationError(self):


        with self.assertRaises(ValidationError):
            ResumeRequest(full_name='Test User', title='Software Engineer', education='Undergraduate degree', summary='Summary of resume', status='Active', employment_type='Full-time', location='Invalid location', skills=['Python', 'Java', 'MySQL'])


    def testCreateResume_InvalidSkill_RaiseValidationError(self):


        with self.assertRaises(ValidationError):
            ResumeRequest(full_name='Test User', title='Software Engineer', education='Undergraduate degree', summary='Summary of resume', status='Active', employment_type='Full-time', location='Sofia', skills=['Invalid skill'])


    def testCreateResume_