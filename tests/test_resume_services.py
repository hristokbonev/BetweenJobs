import os
from unittest import TestCase
from datetime import datetime
from pydantic import ValidationError
from sqlmodel import Session, SQLModel, create_engine, delete, select
from resumes import resume_services as rs
from data.db_models import Resume, ResumeSkill, User, Location, Education, Status, EmploymentType, Skill
from fastapi.testclient import TestClient
from main import app
from resumes.resume_models import ResumeRequest, ResumeResponse, ResumeResponseWithIds, ResumeUpdate

client = TestClient(app)

class TestResumeModels(TestCase):

    @classmethod
    def setUpClass(cls):

        cls.engine = create_engine("sqlite:///testing.db", connect_args={"check_same_thread": False})

        SQLModel.metadata.create_all(cls.engine)
        
    @classmethod
    def tearDownClass(cls):
        try:
            pass
        finally:
            SQLModel.metadata.drop_all(cls.engine)
            cls.engine.dispose()
            if os.path.exists('testing.db'):
                os.remove('testing.db')
            

    def setUp(self):

        self.session = Session(self.engine)

        self.testuser = User(id=1, username='testuser', email='testuser@email.com',
                                        first_name='Test', last_name='User', created_at=datetime.strptime('2021-01-01', '%Y-%m-%d'),
                                        is_admin=False, date_of_birth=datetime.strptime('1990-01-01', '%Y-%m-%d'), employer_id=None, password='password')
        
        self.testlocattion = Location(id=1, name='Sofia')
        self.testlocation2 = Location(id=2, name='Plovdiv')

        self.testeducation = Education(id=1, degree_level='Undergraduate degree')
        self.testeducation2 = Education(id=2, degree_level='High school')

        self.teststatus = Status(id=1, name='Active')
        self.teststatus2 = Status(id=2, name='Hidden')

        self.testemploymenttype = EmploymentType(id=1, name='Full-time')
        self.testemploymenttype2 = EmploymentType(id=2, name='Part-time')

        self.testskill = Skill(id=1, name='Python')
        self.testskill2 = Skill(id=2, name='Java')
        self.testskill3 = Skill(id=3, name='MySQL')

        self.testresume = Resume(user_id=1, full_name='Test User', title='Software Engineer', education_id=1, summary='Summary of resume', location_id=1, status_id=1, employment_type_id=1, id=1)
        self.testresumeskill1 = ResumeSkill(resume_id=1, skill_id=1)
        self.testresumeskill2 = ResumeSkill(resume_id=1, skill_id=2)
        self.testresumeskill3 = ResumeSkill(resume_id=1, skill_id=3)

        self.testresumenoskills = Resume(user_id=1, full_name='Test User', title='Software Engineer', education_id=1, summary='Summary of resume', location_id=1, status_id=1, employment_type_id=1, id=1)
        
        self.testresume2 = Resume(user_id=1, full_name='Test User', title='Data Scientist', education_id=2, summary='Summary of resume', location_id=2, status_id=2, employment_type_id=2, id=2)

        self.testresume3 = Resume(user_id=1, full_name='Test Professional', title='Software Develper', education_id=1, summary='Summary of resume', location_id=1, status_id=1, employment_type_id=1, id=3)
        self.testresume3skill = ResumeSkill(resume_id=3, skill_id=1)
        self.testresume3skill2 = ResumeSkill(resume_id=3, skill_id=2)
        self.testresume3skill3 = ResumeSkill(resume_id=3, skill_id=3)

        self.session.exec(delete(ResumeSkill))
        self.session.exec(delete(Resume))
        self.session.exec(delete(Skill))
        self.session.exec(delete(Location))
        self.session.exec(delete(Education))
        self.session.exec(delete(Status))
        self.session.exec(delete(EmploymentType))
        self.session.exec(delete(User))
        self.session.commit()
               
        self.session.add_all([self.testuser, self.testlocattion, self.testlocation2, 
                              self.testeducation, self.testeducation2, self.teststatus, 
                              self.teststatus2, self.testemploymenttype, self.testemploymenttype2, 
                              self.testskill, self.testskill2, self.testskill3])

        self.session.commit()

    def tearDown(self):

        try:
            pass
        finally:
            self.session.exec(delete(ResumeSkill))
            self.session.exec(delete(Resume))
            self.session.exec(delete(Skill))
            self.session.exec(delete(Location))
            self.session.exec(delete(Education))
            self.session.exec(delete(Status))
            self.session.exec(delete(EmploymentType))
            self.session.exec(delete(User))        
            self.session.commit()
            self.session.close()

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

    def testGetResumeById_ExistingId_ReturnResumeResponse(self):

        self.session.add(self.testresume)
        self.session.add(self.testresumeskill1)
        self.session.add(self.testresumeskill2)
        self.session.add(self.testresumeskill3)
        self.session.commit()

        resume = rs.get_resume_by_id(session=self.session, id=1)

        expected = ResumeResponse(id=1, user_id=1, full_name='Test User', title='Software Engineer', summary='Summary of resume',
                                  username='testuser', employment_type='Full-time', education='Undergraduate degree', location='Sofia',
                                  status='Active', skills=['Python', 'Java', 'MySQL'])

        self.assertEqual(resume, expected)


    def testGetResumeById_NonExisting_ReturnNone(self):

        resumes = rs.get_resume_by_id(session=self.session, id=2)

        self.assertIsNone(resumes)


    def testGetResumeById_InvalidId_ReturnNone(self):

        resumes = rs.get_resume_by_id(session=self.session, id='string')

        self.assertIsNone(resumes)

    def testGetResumeById_NoSkills_RetrunsResumeResponse(self):

        self.session.add(self.testresumenoskills)
        self.session.commit()

        resumes = rs.get_resume_by_id(session=self.session, id=1)

        expected = ResumeResponse(id=1, user_id=1, full_name='Test User', title='Software Engineer', summary='Summary of resume',
                                  username='testuser', employment_type='Full-time', education='Undergraduate degree', location='Sofia',
                                  status='Active', skills=[])

        self.assertEqual(resumes, expected)

    def testGetAllResumes_ReturnsListOfResumes(self):

        self.session.add(self.testresume)
        self.session.add(self.testresumeskill1)
        self.session.add(self.testresumeskill2)
        self.session.add(self.testresumeskill3)
        self.session.add(self.testresume2)
        self.session.commit()

        resumes = rs.get_all_resumes(session=self.session)

        expected = [ResumeResponse(id=1, user_id=1, full_name='Test User', title='Software Engineer', summary='Summary of resume',
                                   username='testuser', employment_type='Full-time', education='Undergraduate degree', location='Sofia',
                                   status='Active', skills=['Python', 'Java', 'MySQL']), 
                    ResumeResponse(id=2, user_id=1, full_name='Test User',title='Data Scientist', summary='Summary of resume', 
                                   username='testuser', employment_type='Part-time', education='High school',
                                   location='Plovdiv', status='Hidden', skills=[])]

        self.assertEqual(resumes, expected)

    def testGetAllResumes_NoResumes_ReturnsNone(self):

        self.session.exec(delete(Resume))
        self.session.commit()

        resumes = rs.get_all_resumes(session=self.session)

        self.assertIsNone(resumes)

    def testGetAllResumes_OneResumeDatabasa_ReturnsListWithOneResumeResponse(self):

        self.session.add(self.testresume)
        self.session.add(self.testresumeskill1)
        self.session.add(self.testresumeskill2)
        self.session.add(self.testresumeskill3)
        self.session.commit()

        resumes = rs.get_all_resumes(session=self.session)

        expected = [ResumeResponse(id=1, user_id=1, full_name='Test User', title='Software Engineer', summary='Summary of resume',
                                  username='testuser', employment_type='Full-time', education='Undergraduate degree', location='Sofia',
                                  status='Active', skills=['Python', 'Java', 'MySQL'])]

        self.assertEqual(resumes, expected)

    def testUpdateResume_ExistingResume_UpdatesTitle(self):

        self.session.add(self.testresumenoskills)
        self.session.commit()

        self.assertEqual(self.testresume.title, 'Software Engineer')

        update_form = ResumeUpdate(title='Data Scientist')

        updated_resume = rs.update_resume(session=self.session, id=1, resume_form=update_form)

        expected = ResumeResponse(id=1, user_id=1, full_name='Test User', title='Data Scientist', summary='Summary of resume',
                                  username='testuser', employment_type='Full-time', education='Undergraduate degree', location='Sofia',
                                  status='Active', skills=[])

        self.assertEqual(updated_resume, expected)

    def testUpdateResume_ExistingResume_UpdatesSummary(self):

        self.session.add(self.testresumenoskills)
        self.session.commit()

        self.assertEqual(self.testresume.summary, 'Summary of resume')

        update_form = ResumeUpdate(summary='New summary')


        updated_resume = rs.update_resume(session=self.session, id=1, resume_form=update_form)

        expected = ResumeResponse(id=1, user_id=1, full_name='Test User', title='Software Engineer', summary='New summary',
                                  username='testuser', employment_type='Full-time', education='Undergraduate degree', location='Sofia',
                                  status='Active', skills=[])

        self.assertEqual(updated_resume, expected)

    def testUpdateResume_ExistingResume_UpdatesLocation(self):

        self.session.add(self.testresumenoskills)
        self.session.commit()

        self.assertEqual(self.testresume.location_id, 1)

        update_form = ResumeUpdate(location='Plovdiv')

        updated_resume = rs.update_resume(session=self.session, id=1, resume_form=update_form)

        expected = ResumeResponse(id=1, user_id=1, full_name='Test User', title='Software Engineer', summary='Summary of resume',
                                  username='testuser', employment_type='Full-time', education='Undergraduate degree', location='Plovdiv',
                                  status='Active', skills=[])

        self.assertEqual(updated_resume, expected)

    def testUpdateResume_ExistingResume_UpdatesEducation(self):

        self.session.add(self.testresumenoskills)
        self.session.commit()

        self.assertEqual(self.testresume.education_id, 1)

        update_form = ResumeUpdate(education='High school')

        updated_resume = rs.update_resume(session=self.session, id=1, resume_form=update_form)

        expected = ResumeResponse(id=1, user_id=1, full_name='Test User', title='Software Engineer', summary='Summary of resume',
                                  username='testuser', employment_type='Full-time', education='High school', location='Sofia',
                                  status='Active', skills=[])

        self.assertEqual(updated_resume, expected)

    def testUpdateResume_ExistingResume_UpdatesEmploymentType(self):

        self.session.add(self.testresumenoskills)
        self.session.commit()

        self.assertEqual(self.testresume.employment_type_id, 1)

        update_form = ResumeUpdate(employment_type='Part-time')

        updated_resume = rs.update_resume(session=self.session, id=1, resume_form=update_form)

        expected = ResumeResponse(id=1, user_id=1, full_name='Test User', title='Software Engineer', summary='Summary of resume',
                                  username='testuser', employment_type='Part-time', education='Undergraduate degree', location='Sofia',
                                  status='Active', skills=[])

        self.assertEqual(updated_resume, expected)

    def testUpdateResume_ExistingResume_UpdatesStatus(self):
            
            self.session.add(self.testresumenoskills)
            self.session.commit()
    
            self.assertEqual(self.testresume.status_id, 1)
    
            update_form = ResumeUpdate(status='Hidden')
    
            updated_resume = rs.update_resume(session=self.session, id=1, resume_form=update_form)
    
            expected = ResumeResponse(id=1, user_id=1, full_name='Test User', title='Software Engineer', summary='Summary of resume',
                                    username='testuser', employment_type='Full-time', education='Undergraduate degree', location='Sofia',
                                    status='Hidden', skills=[])
    
            self.assertEqual(updated_resume, expected)


    def testUpdateResume_ExistingResume_UpdatesSkills(self):
            
            self.session.add(self.testresumenoskills)
            self.session.commit()
    
            self.assertEqual(self.testresume.skills, [])
    
            update_form = ResumeUpdate(skills=['Python', 'Java', 'MySQL'])
    
            updated_resume = rs.update_resume(session=self.session, id=1, resume_form=update_form)
    
            expected = ResumeResponse(id=1, user_id=1, full_name='Test User', title='Software Engineer', summary='Summary of resume',
                                    username='testuser', employment_type='Full-time', education='Undergraduate degree', location='Sofia',
                                    status='Active', skills=['Python', 'Java', 'MySQL'])
    
            self.assertEqual(updated_resume, expected)

    def testUpdateResume_ExistingResume_UpdatesMultipleFields(self):

        self.session.add(self.testresumenoskills)
        self.session.commit()

        self.assertEqual(self.testresume.title, 'Software Engineer')
        self.assertEqual(self.testresume.summary, 'Summary of resume')
        self.assertEqual(self.testresume.location_id, 1)
        self.assertEqual(self.testresume.education_id, 1)
        self.assertEqual(self.testresume.employment_type_id, 1)
        self.assertEqual(self.testresume.status_id, 1)
        self.assertEqual(self.testresume.skills, [])

        update_form = ResumeUpdate(title='Data Scientist', summary='New summary', location='Plovdiv', education='High school', employment_type='Part-time', status='Hidden', skills=['Python', 'Java', 'MySQL'])

        updated_resume = rs.update_resume(session=self.session, id=1, resume_form=update_form)

        expected = ResumeResponse(id=1, user_id=1, full_name='Test User', title='Data Scientist', summary='New summary',
                                  username='testuser', employment_type='Part-time', education='High school', location='Plovdiv',
                                  status='Hidden', skills=['Python', 'Java', 'MySQL'])

        self.assertEqual(updated_resume, expected)

    
    def testUpdateResume_NonExistingResume_ReturnsNone(self):

        update_form = ResumeUpdate(title='Data Scientist')

        updated_resume = rs.update_resume(session=self.session, id=1, resume_form=update_form)

        self.assertIsNone(updated_resume)

    def testUpdateResume_InvalidId_ReturnsNone(self):
            
            update_form = ResumeUpdate(title='Data Scientist')
    
            updated_resume = rs.update_resume(session=self.session, id='string', resume_form=update_form)
    
            self.assertIsNone(updated_resume)

    def testUpdateResume_InvalidEducation_RaiseValidationError(self):
    
            with self.assertRaises(ValidationError):
                ResumeUpdate(education='Invalid education')

    def testUpdateResume_InvalidStatus_RaiseValidationError(self):

        with self.assertRaises(ValidationError):
            ResumeUpdate(status='Invalid status')

    def testUpdateResume_InvalidEmploymentType_RaiseValidationError(self):

        with self.assertRaises(ValidationError):
            ResumeUpdate(employment_type='Invalid employment type')

    def testUpdateResume_InvalidLocation_RaiseValidationError(self):

        with self.assertRaises(ValidationError):
            ResumeUpdate(location='Invalid location')

    def testUpdateResume_InvalidSkill_RaiseValidationError(self):

        with self.assertRaises(ValidationError):
            ResumeUpdate(skills=['Invalid skill'])

    def testDeleteResume_NonExistingId_ReturnsNone(self):

        deleted = rs.delete_resume(session=self.session, id=1)

        self.assertIsNone(deleted)

    def testDeleteResume_ExistingId_DeletesResume(self):

        self.session.add(self.testresumenoskills)
        self.session.commit()

        self.assertIsNotNone(rs.get_resume_by_id(session=self.session, id=1))

        rs.delete_resume(session=self.session, id=1)

        self.assertIsNone(rs.get_resume_by_id(session=self.session, id=1))

    def testDeleteResume_InvalidId_ReturnsNone(self):

        deleted = rs.delete_resume(session=self.session, id='string')

        self.assertIsNone(deleted)

    def testGetResumeWithIdsInsteadOfNames_ReturnsResumeResponse(self):

        self.session.add(self.testresume)
        self.session.add(self.testresumeskill1)
        self.session.add(self.testresumeskill2)
        self.session.add(self.testresumeskill3)
        self.session.commit()

        resume = rs.get_resume_with_ids_instead_of_names(session=self.session, id=1)

        expected = ResumeResponseWithIds(id=1, user_id=1, full_name='Test User', title='Software Engineer', summary='Summary of resume',
                                  employment_type=1, education=1, location=1, status=1, skills=[1, 2, 3])

        self.assertEqual(resume, expected)

    def testGetResumeWithIdsInsteadOfNames_NonExistingId_ReturnsNone(self):
            
        resume = rs.get_resume_with_ids_instead_of_names(session=self.session, id=2)

        self.assertIsNone(resume)

    def testGetResumeWithIdsInsteadOfNames_InvalidId_ReturnsNone(self):

        resume = rs.get_resume_with_ids_instead_of_names(session=self.session, id='string')

        self.assertIsNone(resume)

    def testGetResumeWithIdsInsteadOfNames_NoSkills_ReturnsResumeResponseWithEmptySkillList(self):

        self.session.add(self.testresumenoskills)
        self.session.commit()

        resume = rs.get_resume_with_ids_instead_of_names(session=self.session, id=1)

        expected = ResumeResponseWithIds(id=1, user_id=1, full_name='Test User', title='Software Engineer', summary='Summary of resume',
                                  employment_type=1, education=1, location=1, status=1, skills=[])

        self.assertEqual(resume, expected)

    def testGetAllResumes_SearchByTitle_ReturnsListOfResumes(self):

        self.session.add(self.testresume)
        self.session.add(self.testresumeskill1)
        self.session.add(self.testresumeskill2)
        self.session.add(self.testresumeskill3)
        self.session.add(self.testresume2)
        self.session.add(self.testresume3)
        self.session.commit()

        resumes = self.session.exec(select(Resume)).all()

        self.assertEqual(len(resumes), 3)

        resumes = rs.get_all_resumes(session=self.session, title='Software')

        expected = [ResumeResponse(id=1, user_id=1, full_name='Test User', title='Software Engineer', summary='Summary of resume',
                                username='testuser', employment_type='Full-time', education='Undergraduate degree', location='Sofia',
                                status='Active', skills=['Python', 'Java', 'MySQL']),
                    ResumeResponse(id=3, user_id=1, full_name='Test Professional', title='Software Develper', summary='Summary of resume',
                                   username='testuser', employment_type='Full-time', education='Undergraduate degree', location='Sofia',
                                status='Active', skills=[])]

        self.assertEqual(resumes, expected)


    def testGetAllResumes_SearchByTitle_NoResumesFound_ReturnsNone(self):

        self.session.add(self.testresumenoskills)

        self.session.commit()

        resumes = self.session.exec(select(Resume)).all()

        self.assertEqual(len(resumes), 1)

        resumes = rs.get_all_resumes(session=self.session, title='Data Scientist')

        self.assertIsNone(resumes)

    def testGetAllResumes_SearchByLocation_ReturnsListOfResumes(self):

        self.session.add(self.testresume)
        self.session.add(self.testresumeskill1)
        self.session.add(self.testresumeskill2)
        self.session.add(self.testresumeskill3)
        self.session.add(self.testresume2)
        self.session.add(self.testresume3)
        self.session.commit()

        resumes = self.session.exec(select(Resume)).all()

        self.assertEqual(len(resumes), 3)

        resumes = rs.get_all_resumes(session=self.session, location='Sofia')

        expected = [ResumeResponse(id=1, user_id=1, full_name='Test User', title='Software Engineer', summary='Summary of resume',
                                username='testuser', employment_type='Full-time', education='Undergraduate degree', location='Sofia',
                                status='Active', skills=['Python', 'Java', 'MySQL']),
                    ResumeResponse(id=3, user_id=1, full_name='Test Professional', title='Software Develper', summary='Summary of resume',
                                   username='testuser', employment_type='Full-time', education='Undergraduate degree', location='Sofia',
                                status='Active', skills=[])]

        self.assertEqual(resumes, expected)

    def testGetAllResumes_SearchByLocation_NoResumesFound_ReturnsNone(self):

        self.session.add(self.testresumenoskills)
        self.session.commit()

        resumes = self.session.exec(select(Resume)).all()

        self.assertEqual(len(resumes), 1)

        resumes = rs.get_all_resumes(session=self.session, location='Plovdiv')

        self.assertIsNone(resumes)

    def testGetAllResumes_SearchByEmploymentType_ReturnsListOfResumes(self):

        self.session.add(self.testresume)
        self.session.add(self.testresumeskill1)
        self.session.add(self.testresumeskill2)
        self.session.add(self.testresumeskill3)
        self.session.add(self.testresume2)
        self.session.add(self.testresume3)
        self.session.commit()

        resumes = self.session.exec(select(Resume)).all()

        self.assertEqual(len(resumes), 3)

        resumes = rs.get_all_resumes(session=self.session, employment_type='Full-time')

        expected = [ResumeResponse(id=1, user_id=1, full_name='Test User', title='Software Engineer', summary='Summary of resume',
                                username='testuser', employment_type='Full-time', education='Undergraduate degree', location='Sofia',
                                status='Active', skills=['Python', 'Java', 'MySQL']),
                    ResumeResponse(id=3, user_id=1, full_name='Test Professional', title='Software Develper', summary='Summary of resume',
                                   username='testuser', employment_type='Full-time', education='Undergraduate degree', location='Sofia',
                                status='Active', skills=[])]

        self.assertEqual(resumes, expected)

    def testGetAllResumes_SearchByEmploymentType_NoResumesFound_ReturnsNone(self):
            
            self.session.add(self.testresume)
            self.session.add(self.testresumeskill1)
            self.session.add(self.testresumeskill2)
            self.session.add(self.testresumeskill3)
            self.session.commit()
    
            resumes = self.session.exec(select(Resume)).all()
    
            self.assertEqual(len(resumes), 1)
    
            resumes = rs.get_all_resumes(session=self.session, employment_type='Part-time')
    
            self.assertIsNone(resumes)

    def testGetAllResumes_SearchByEducation_ReturnsListOfResumes(self):

        self.session.add(self.testresume)
        self.session.add(self.testresumeskill1)
        self.session.add(self.testresumeskill2)
        self.session.add(self.testresumeskill3)
        self.session.add(self.testresume2)
        self.session.add(self.testresume3)
        self.session.commit()

        resumes = self.session.exec(select(Resume)).all()

        self.assertEqual(len(resumes), 3)

        resumes = rs.get_all_resumes(session=self.session, education='Undergraduate degree')

        expected = [ResumeResponse(id=1, user_id=1, full_name='Test User', title='Software Engineer', summary='Summary of resume',
                                username='testuser', employment_type='Full-time', education='Undergraduate degree', location='Sofia',
                                status='Active', skills=['Python', 'Java', 'MySQL']),
                    ResumeResponse(id=3, user_id=1, full_name='Test Professional', title='Software Develper', summary='Summary of resume',
                                   username='testuser', employment_type='Full-time', education='Undergraduate degree', location='Sofia',
                                status='Active', skills=[])]

        self.assertEqual(resumes, expected)


    def testGetAllResumes_SearchByEducation_NoResumesFound_ReturnsNone(self):

        self.session.add(self.testresumenoskills)
        self.session.commit()

        resumes = self.session.exec(select(Resume)).all()

        self.assertEqual(len(resumes), 1)

        resumes = rs.get_all_resumes(session=self.session, education='High school')

        self.assertIsNone(resumes)

    def testGetAllResumes_SearchByStatus_ReturnsListOfResumes(self):

        self.session.add(self.testresume)
        self.session.add(self.testresumeskill1)
        self.session.add(self.testresumeskill2)
        self.session.add(self.testresumeskill3)
        self.session.add(self.testresume2)
        self.session.add(self.testresume3)
        self.session.commit()

        resumes = self.session.exec(select(Resume)).all()

        self.assertEqual(len(resumes), 3)

        resumes = rs.get_all_resumes(session=self.session, status='Active')

        expected = [ResumeResponse(id=1, user_id=1, full_name='Test User', title='Software Engineer', summary='Summary of resume',
                                username='testuser', employment_type='Full-time', education='Undergraduate degree', location='Sofia',
                                status='Active', skills=['Python', 'Java', 'MySQL']),
                    ResumeResponse(id=3, user_id=1, full_name='Test Professional', title='Software Develper', summary='Summary of resume',
                                   username='testuser', employment_type='Full-time', education='Undergraduate degree', location='Sofia',
                                status='Active', skills=[])]

        self.assertEqual(resumes, expected)


    def testGetAllResumes_SearchByStatus_NoResumesFound_ReturnsNone(self):

        self.session.add(self.testresumenoskills)
        self.session.commit()

        resumes = self.session.exec(select(Resume)).all()

        self.assertEqual(len(resumes), 1)

        resumes = rs.get_all_resumes(session=self.session, status='Hidden')

        self.assertIsNone(resumes)

    def testGetAllResumes_SearchBySkills_ReturnsListOfResumes(self):

        self.session.add(self.testresume)
        self.session.add(self.testresumeskill1)
        self.session.add(self.testresumeskill2)
        self.session.add(self.testresumeskill3)
        self.session.add(self.testresume2)
        self.session.add(self.testresume3)
        self.session.add(self.testresume3skill)
        self.session.commit()

        resumes = self.session.exec(select(Resume)).all()

        self.assertEqual(len(resumes), 3)

        resumes = rs.get_all_resumes(session=self.session, skills=['Python', 'Java'])

        expected = [ResumeResponse(id=1, user_id=1, full_name='Test User', title='Software Engineer', summary='Summary of resume',
                                username='testuser', employment_type='Full-time', education='Undergraduate degree', location='Sofia',
                                status='Active', skills=['Python', 'Java', 'MySQL'])]

        self.assertEqual(resumes, expected)

    def testGetAllResumes_SearchBySkillResumesShareSkill_ReturnsListOfResumes(self):

        self.session.add(self.testresume)
        self.session.add(self.testresumeskill1)
        self.session.add(self.testresumeskill2)
        self.session.add(self.testresumeskill3)
        self.session.add(self.testresume2)
        self.session.add(self.testresume3)
        self.session.add(self.testresume3skill)
        self.session.commit()

        resumes = self.session.exec(select(Resume)).all()

        self.assertEqual(len(resumes), 3)

        resumes = rs.get_all_resumes(session=self.session, skills=['Python'])

        expected = [ResumeResponse(id=3, user_id=1, full_name='Test Professional', title='Software Develper', summary='Summary of resume',
                                   username='testuser', employment_type='Full-time', education='Undergraduate degree', location='Sofia',
                                status='Active', skills=['Python']),
                    ResumeResponse(id=1, user_id=1, full_name='Test User', title='Software Engineer', summary='Summary of resume',
                                username='testuser', employment_type='Full-time', education='Undergraduate degree', location='Sofia',
                                status='Active', skills=['Python', 'Java', 'MySQL'])]

        self.assertEqual(resumes, expected)

    def testGetAllResumes_SearchBySkills_NoResumesFound_ReturnsNone(self):

        self.session.add(self.testresumenoskills)
        self.session.commit()

        resumes = self.session.exec(select(Resume)).all()

        self.assertEqual(len(resumes), 1)

        resumes = rs.get_all_resumes(session=self.session, skills=['Java'])

        self.assertIsNone(resumes)

    def testGetAllResumes_SearchByMultipleFields_ReturnsListOfResumes(self):
            
            self.session.add(self.testresume)
            self.session.add(self.testresumeskill1)
            self.session.add(self.testresumeskill2)
            self.session.add(self.testresumeskill3)
            self.session.add(self.testresume2)
            self.session.add(self.testresume3)
            self.session.commit()
    
            resumes = self.session.exec(select(Resume)).all()
    
            self.assertEqual(len(resumes), 3)
    
            resumes = rs.get_all_resumes(session=self.session, title='Software', location='Sofia')
    
            expected = [ResumeResponse(id=1, user_id=1, full_name='Test User', title='Software Engineer', summary='Summary of resume',
                                    username='testuser', employment_type='Full-time', education='Undergraduate degree', location='Sofia',
                                    status='Active', skills=['Python', 'Java', 'MySQL']),
                        ResumeResponse(id=3, user_id=1, full_name='Test Professional', title='Software Develper', summary='Summary of resume',
                                    username='testuser', employment_type='Full-time', education='Undergraduate degree', location='Sofia',
                                    status='Active', skills=[])]
    
            self.assertEqual(resumes, expected)


    def testGetAllResumes_SearchByMultipleFields_NoResumesFound_ReturnsNone(self):

        self.session.add(self.testresumenoskills)
        self.session.commit()

        resumes = self.session.exec(select(Resume)).all()

        self.assertEqual(len(resumes), 1)

        resumes = rs.get_all_resumes(session=self.session, title='Data Scientist', location='Plovdiv')

        self.assertIsNone(resumes)

    def testGetAllResumes_SearchByName_ReturnsListOfResumes(self):

        self.session.add(self.testresume)
        self.session.add(self.testresumeskill1)
        self.session.add(self.testresumeskill2)
        self.session.add(self.testresumeskill3)
        self.session.add(self.testresume2)
        self.session.add(self.testresume3)
        self.session.commit()

        resumes = self.session.exec(select(Resume)).all()

        self.assertEqual(len(resumes), 3)

        resumes = rs.get_all_resumes(session=self.session, name='Test User')

        expected = [ResumeResponse(id=1, user_id=1, full_name='Test User', title='Software Engineer', summary='Summary of resume',
                                username='testuser', employment_type='Full-time', education='Undergraduate degree', location='Sofia',
                                status='Active', skills=['Python', 'Java', 'MySQL']),
                    ResumeResponse(id=2, user_id=1, full_name='Test User', title='Data Scientist', summary='Summary of resume',
                                username='testuser', employment_type='Part-time', education='High school', location='Plovdiv',
                                status='Hidden', skills=[])]

        self.assertEqual(resumes, expected)


    def testGetAllResumes_SearchByName_NoResumesFound_ReturnsNone(self):

        self.session.add(self.testresumenoskills)
        self.session.commit()

        resumes = self.session.exec(select(Resume)).all()

        self.assertEqual(len(resumes), 1)

        resumes = rs.get_all_resumes(session=self.session, name='Test Professional')

        self.assertIsNone(resumes)


    def testGetAllResumesWithSkillsIds_NoResumes_ReturnsNone(self):

        resumes = rs.get_all_resumes_with_skills_ids(session=self.session)

        self.assertIsNone(resumes)

    def testGetAllResumesWithSkillsIds_ReturnsListOfResumes(self):

        self.session.add(self.testresume)
        self.session.add(self.testresumeskill1)
        self.session.add(self.testresumeskill2)
        self.session.add(self.testresumeskill3)
        self.session.add(self.testresume2)

        self.session.commit()

        resumes = self.session.exec(select(Resume)).all()

        self.assertEqual(len(resumes), 2)

        resumes = rs.get_all_resumes_with_skills_ids(session=self.session)

        expected = [ResumeResponseWithIds(id=1, user_id=1, full_name='Test User', title='Software Engineer', summary='Summary of resume',
                                  employment_type=1, education=1, location=1, status=1, skills=[1, 2, 3]),
                    ResumeResponseWithIds(id=2, user_id=1, full_name='Test User', title='Data Scientist', summary='Summary of resume',
                                  employment_type=2, education=2, location=2, status=2, skills=[])]
        
        self.assertEqual(resumes, expected)