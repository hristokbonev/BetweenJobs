from unittest import TestCase
from sqlmodel import create_engine, Session, delete
from data.db_models import Company, JobAd, JobAdSkill, User, Location, Education, Status, EmploymentType, Skill, Resume, ResumeSkill
from sqlmodel import SQLModel
import os
from jobposts.jobpost_models import JobAdResponseWithNamesNotId
from matches.match_services import suggest_job_ads, suggest_resumes, titles_match
from datetime import datetime
from resumes.resume_models import ResumeResponse

class TestMatchServices(TestCase):

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

        self.testuser = User(id=1, username='testuser', email='testuser@email.com',
                                        first_name='Test', last_name='User', created_at=datetime.strptime('2021-01-01', '%Y-%m-%d'),
                                        is_admin=False, date_of_birth=datetime.strptime('1990-01-01', '%Y-%m-%d'), employer_id=None, password='password')
        
        self.testcompany = Company(id=1, created_at=datetime.strptime('2021-01-01', '%Y-%m-%d'), name='Test Company', description='Test Description', author_id=1)

        self.testlocattion = Location(id=1, name='Sofia')
        self.testlocation2 = Location(id=2, name='Plovdiv')

        self.testeducation = Education(id=1, degree_level='Undergraduate degree')
        self.testeducation2 = Education(id=2, degree_level='Postgraduate degree')

        self.teststatus = Status(id=1, name='Active')
        self.teststatus2 = Status(id=2, name='Hidden')

        self.testemploymenttype = EmploymentType(id=1, name='Full-time')
        self.testemploymenttype2 = EmploymentType(id=2, name='Part-time')

        self.testskill = Skill(id=1, name='Python')
        self.testskill2 = Skill(id=2, name='Java')
        self.testskill3 = Skill(id=3, name='MySQL')
        self.testskill4 = Skill(id=4, name='JavaScript')    

        self.testskill5 = Skill(id=5, name='Bussiness Development')
        self.testskill6 = Skill(id=6, name='Marketing')
        self.testskill7 = Skill(id=7, name='Sales')
        self.testskill8 = Skill(id=8, name='Management')

        self.testskill9 = Skill(id=9, name='Data Science')
        self.testskill10 = Skill(id=10, name='Machine Learning')
        self.testskill11 = Skill(id=11, name='Artificial Intelligence')
        self.testskill12 = Skill(id=12, name='Algorithms')

        # Resume 1 - Software Engineer
        self.testresume = Resume(id=1, title='Software Engineer', user_id=1, location_id=1, education_id=1, status_id=1, employment_type_id=1)
        self.resume_skill = ResumeSkill(resume_id=1, skill_id=1)  # Python
        self.resume_skill2 = ResumeSkill(resume_id=1, skill_id=2)  # Java
        self.resume_skill3 = ResumeSkill(resume_id=1, skill_id=3)  # MySQL
        self.resume_skill4 = ResumeSkill(resume_id=1, skill_id=4)  # JavaScript

        # Resume 2 - Web Developer
        self.testresume2 = Resume(id=2, title='Web Developer', user_id=1, location_id=1, education_id=1, status_id=1, employment_type_id=1)
        self.resume2skill = ResumeSkill(resume_id=2, skill_id=1)  # Python
        self.resume2skill2 = ResumeSkill(resume_id=2, skill_id=2)  # Java

        # Resume 3 - Data Scientist
        self.testresume3 = Resume(id=3, title='Data Scientist', user_id=1, location_id=1, education_id=1, status_id=1, employment_type_id=1)
        self.resume3skill = ResumeSkill(resume_id=3, skill_id=9)  # Data Science
        self.resume3skill2 = ResumeSkill(resume_id=3, skill_id=10)  # Machine Learning

        # Resume 4 - Machine Learning Engineer
        self.testresume4 = Resume(id=4, title='Machine Learning Engineer', user_id=1, location_id=1, education_id=1, status_id=1, employment_type_id=1)
        self.resume4skill = ResumeSkill(resume_id=4, skill_id=9)  # Data Science
        self.resume4skill2 = ResumeSkill(resume_id=4, skill_id=10)  # Machine Learning
        self.resume4skill3 = ResumeSkill(resume_id=4, skill_id=11)  # Artificial Intelligence
        self.resume4skill4 = ResumeSkill(resume_id=4, skill_id=12)  # Algorithms

        # Resume 5 - Sales Executive
        self.testresume5 = Resume(id=5, title='Sales Executive', user_id=1, location_id=1, education_id=1, status_id=1, employment_type_id=1)
        self.resume5skill = ResumeSkill(resume_id=5, skill_id=5)  # Business Development
        self.resume5skill2 = ResumeSkill(resume_id=5, skill_id=6)  # Marketing
        self.resume5skill3 = ResumeSkill(resume_id=5, skill_id=7)  # Sales
        self.resume5skill4 = ResumeSkill(resume_id=5, skill_id=8)  # Management

        # Resume 6 - Business Development Manager
        self.testresume6 = Resume(id=6, title='Business Development Manager', user_id=1, location_id=1, education_id=1, status_id=1, employment_type_id=1)
        self.resume6skill = ResumeSkill(resume_id=6, skill_id=5)  # Business Development
    
        
        # Job Ad 1 - Software Engineer
        self.testjobad = JobAd(title='Software Engineer', company_id=1, company_name='Test Company', description='Test Description', education_id=1, salary=2000.00, employment_type_id=1, location_id=1, status_id=1, created_at=datetime.strptime('2024-11-28', '%Y-%m-%d'))

        self.jobad_skill = JobAdSkill(jobad_id=1, skill_id=1)  # Python
        self.jobad_skill2 = JobAdSkill(jobad_id=1, skill_id=2)  # Java
        self.jobad_skill3 = JobAdSkill(jobad_id=1, skill_id=3)  # MySQL
        self.jobad_skill4 = JobAdSkill(jobad_id=1, skill_id=4)  # JavaScript

        # Job Ad 2 - Web Developer
        self.testjobad2 = JobAd(id=2, title='Web Developer', location_id=1, education_id=1, employment_type_id=1, company_id=1, company_name='Test Company', description='Test Description', salary=2000.00, status_id=1, created_at=datetime.strptime('2024-11-28', '%Y-%m-%d'))
        self.jobad2skill = JobAdSkill(jobad_id=2, skill_id=1)  # Python
        self.jobad2skill2 = JobAdSkill(jobad_id=2, skill_id=2)  # Java

        # Job Ad 3 - Data Scientist
        self.testjobad3 = JobAd(id=3, title='Data Scientist', location_id=1, education_id=1, employment_type_id=1, company_id=1, company_name='Test Company', description='Test Description', salary=2000.00, status_id=1, created_at=datetime.strptime('2024-11-28', '%Y-%m-%d'))
        self.jobad3skill = JobAdSkill(jobad_id=3, skill_id=9)  # Data Science
        self.jobad3skill2 = JobAdSkill(jobad_id=3, skill_id=10)  # Machine Learning
        self.jobad3skill3 = JobAdSkill(jobad_id=3, skill_id=11)  # Artificial Intelligence

        # Job Ad 4 - Machine Learning Engineer
        self.testjobad4 = JobAd(id=4, title='Machine Learning Engineer', location_id=2, education_id=2, employment_type_id=2, company_id=1, company_name='Test Company', description='Test Description', salary=2000.00, status_id=1, created_at=datetime.strptime('2024-11-28', '%Y-%m-%d'))
        self.jobad4skill = JobAdSkill(jobad_id=4, skill_id=9)  # Data Science
        self.jobad4skill2 = JobAdSkill(jobad_id=4, skill_id=10)  # Machine Learning
        self.jobad4skill3 = JobAdSkill(jobad_id=4, skill_id=11)  # Artificial Intelligence
        self.jobad4skill4 = JobAdSkill(jobad_id=4, skill_id=12)  # Algorithms

        # Job Ad 5 - Business Development Manager
        self.testjobad5 = JobAd(id=5, title='Business Development Manager', location_id=1, education_id=1, employment_type_id=1, company_id=1, company_name='Test Company', description='Test Description', salary=2000.00, status_id=1, created_at=datetime.strptime('2024-11-28', '%Y-%m-%d'))
        self.jobad5skill = JobAdSkill(jobad_id=5, skill_id=5)  # Business Development
        self.jobad5skill2 = JobAdSkill(jobad_id=5, skill_id=6)  # Marketing
        self.jobad5skill3 = JobAdSkill(jobad_id=5, skill_id=7)  # Sales
        self.jobad5skill4 = JobAdSkill(jobad_id=5, skill_id=8)  # Management

        # Job Ad 6 - Business Development Manager
        self.testjobad6 = JobAd(id=6, title='Business Development Manager', location_id=2, education_id=2, employment_type_id=2, company_id=1, company_name='Test Company', description='Test Description', salary=2000.00, status_id=1, created_at=datetime.strptime('2024-11-28', '%Y-%m-%d'))
        self.jobad6skill = JobAdSkill(jobad_id=6, skill_id=5)
        self.jobad6skill2 = JobAdSkill(jobad_id=6, skill_id=6)
        self.jobad6skill3 = JobAdSkill(jobad_id=6, skill_id=7)

        self.testjobad7 = JobAd(id=7, title='Personal Driver', location_id=1, education_id=1, employment_type_id=1, company_id=1, company_name='Test Company', description='Test Description', salary=2000.00, status_id=1, created_at=datetime.strptime('2024-11-28', '%Y-%m-%d'))
        self.testresume7 = Resume(id=7, title='Massage Therapist', user_id=1, location_id=1, education_id=1, status_id=1, employment_type_id=1)


        self.session = Session(self.engine)

        self.session.exec(delete(ResumeSkill))
        self.session.exec(delete(JobAdSkill))
        self.session.exec(delete(JobAd))
        self.session.exec(delete(Resume))
        self.session.exec(delete(Skill))
        self.session.exec(delete(Location))
        self.session.exec(delete(Education))
        self.session.exec(delete(Status))
        self.session.exec(delete(EmploymentType))
        self.session.exec(delete(Company))
        self.session.exec(delete(User))
        self.session.commit()

        self.session.add_all([
        self.testuser, self.testcompany, self.testlocattion, self.testlocation2, self.testeducation, self.testeducation2,
        self.teststatus, self.teststatus2, self.testemploymenttype, self.testemploymenttype2,
        self.testskill, self.testskill2, self.testskill3, self.testskill4, self.testskill5,
        self.testskill6, self.testskill7, self.testskill8, self.testskill9, self.testskill10,
        self.testskill11, self.testskill12, self.testresume, self.testresume2, self.testresume3,
        self.testresume4, self.testresume5, self.testresume6, self.resume_skill, self.resume_skill2,
        self.resume_skill3, self.resume_skill4, self.resume2skill, self.resume2skill2, self.resume3skill,
        self.resume3skill2, self.resume4skill, self.resume4skill2, self.resume4skill3, self.resume4skill4,
        self.resume5skill, self.resume5skill2, self.resume5skill3, self.resume5skill4, self.resume6skill,
        self.testjobad, self.testjobad2, self.testjobad3, self.testjobad4, self.testjobad5, self.testjobad6,
        self.jobad_skill, self.jobad_skill2, self.jobad_skill3, self.jobad_skill4, self.jobad2skill,
        self.jobad2skill2, self.jobad3skill, self.jobad3skill2, self.jobad3skill3, self.jobad4skill,
        self.jobad4skill2, self.jobad4skill3, self.jobad4skill4, self.jobad5skill, self.jobad5skill2,
        self.jobad5skill3, self.jobad5skill4, self.jobad6skill, self.jobad6skill2, self.jobad6skill3, self.testjobad7, self.testresume7,
        ])

        self.session.commit()



    def tearDown(self):

        try:
            pass
        finally:
            self.session.exec(delete(JobAdSkill))
            self.session.exec(delete(JobAd))
            self.session.exec(delete(ResumeSkill))
            self.session.exec(delete(Resume))
            self.session.exec(delete(Skill))
            self.session.exec(delete(Location))
            self.session.exec(delete(Education))
            self.session.exec(delete(Status))
            self.session.exec(delete(EmploymentType))
            self.session.exec(delete(Company))
            self.session.exec(delete(User))        
            self.session.commit()
            self.session.close()


    def testTitlesMatch_Match_ReturnsTrue(self):

        title1 = "Software Engineer"
        title2 = "Web Developer"
        result = titles_match(title1, title2)
        self.assertTrue(result)

    def testTitlesMatch2_Match_ReturnsTrue(self):

        title1 = "Data Scientist"
        title2 = "Machine Learning Engineer"
        result = titles_match(title1, title2)
        self.assertTrue(result)

    def testTitlesMatch3_Match_ReturnsTrue(self):

        title1 = "Sales Executive"
        title2 = "Business Development Manager"
        result = titles_match(title1, title2)
        self.assertTrue(result)
        

    def testTitlesMatch_DontMatch_ReturnsFalse(self):

        title1 = "Software Engineer"
        title2 = "Marketing Manager"
        result = titles_match(title1, title2)
        self.assertFalse(result)

    def testTitlesMatch2_DontMatch_ReturnsFalse(self):

        title1 = "Data Scientist"
        title2 = "Sales Executive"
        result = titles_match(title1, title2)
        self.assertFalse(result)

    def testTitlesMatch3_DontMatch_ReturnsFalse(self):

        title1 = 'Project Manager'
        title2 = 'Graphic Designer'
        result = titles_match(title1, title2)
        self.assertFalse(result)

    def testSuggestJobAds_NoResume_ReturnsNone(self):

        resume_id = 7
        result = suggest_job_ads(resume_id, self.session)
        self.assertIsNone(result)

    def testSuggestJobAds_NoMatchingAds_ReturnsEmptyList(self):

        resume_id = 7
        result = suggest_job_ads(resume_id, self.session)
        self.assertIsNone(result)

    def testSuggestJobAds_MatchingAds_ReturnsList(self):
            
            resume_id = 1
            result = suggest_job_ads(resume_id, self.session)
    
            exected = [JobAdResponseWithNamesNotId(title='Software Engineer', created_at=datetime(2024, 11, 28, 0, 0),
                                                   company_name='Test Company', description='Test Description', education='Undergraduate degree',
                                                   salary=2000.0, employment='Full-time', location='Sofia', status='Active', 
                                                   skills=['Python', 'Java', 'MySQL', 'JavaScript']), 
                        JobAdResponseWithNamesNotId(title='Web Developer', created_at=datetime(2024, 11, 28, 0, 0), 
                                                    company_name='Test Company', description='Test Description', education='Undergraduate degree',
                                                    salary=2000.0, employment='Full-time', location='Sofia', status='Active', skills=['Python', 'Java'])]
            self.assertEqual(result, exected)

    def testSuggestJobAds_MatchingAds2_ReturnsList(self):
            
            resume_id = 3
            result = suggest_job_ads(resume_id, self.session)
    
            exected = [JobAdResponseWithNamesNotId(title='Data Scientist', created_at=datetime(2024, 11, 28, 0, 0),
                                                   company_name='Test Company', description='Test Description', education='Undergraduate degree',
                                                   salary=2000.0, employment='Full-time', location='Sofia', status='Active', 
                                                   skills=['Data Science', 'Machine Learning', 'Artificial Intelligence'])]
            self.assertEqual(result, exected)

    def testSuggestJobAds_MatchingAds3_ReturnsList(self):
                
        resume_id = 5
        result = suggest_job_ads(resume_id, self.session)

        exected = [JobAdResponseWithNamesNotId(title='Business Development Manager', created_at=datetime(2024, 11, 28, 0, 0), 
        company_name='Test Company', description='Test Description', education='Undergraduate degree', salary=2000.0, 
        employment='Full-time', location='Sofia', status='Active', skills=['Bussiness Development', 'Marketing', 'Sales', 'Management'])]
        
        self.assertEqual(result, exected)

    
    def testSuggestResume_NoJobAds_ReturnsNone(self):

        jobad_id = 7
        result = suggest_resumes(jobad_id, self.session)
        self.assertIsNone(result)

    def testSuggestResume_MatchingResumes_ReturnsList(self):

        jobad_id = 1
        result = suggest_resumes(jobad_id, self.session)

        expected = [ResumeResponse(user_id=1, username='testuser', full_name=None, title='Software Engineer', education='Undergraduate degree', summary=None, status='Active', employment_type='Full-time', location='Sofia', id=1, skills=['Python', 'Java', 'MySQL', 'JavaScript'])]

        self.assertEqual(result, expected)

    def testSuggestResume_MatchingResumes2_ReturnsList(self):
             
        jobad_id = 3
        result = suggest_resumes(jobad_id, self.session)

        expected = [ResumeResponse(user_id=1, username='testuser', full_name=None, title='Data Scientist', education='Undergraduate degree', summary=None, status='Active', employment_type='Full-time', location='Sofia', id=3, skills=['Data Science', 'Machine Learning']),
                    ResumeResponse(user_id=1, username='testuser', full_name=None, title='Machine Learning Engineer', education='Undergraduate degree', summary=None, status='Active', employment_type='Full-time', location='Sofia', id=4, skills=['Data Science', 'Machine Learning', 'Artificial Intelligence', 'Algorithms'])]

        self.assertEqual(result, expected)

    def testSuggestResume_MatchingResumes3_ReturnsList(self):
         
        jobad_id = 5 #
        result = suggest_resumes(jobad_id, self.session)

        expected = [ResumeResponse(user_id=1, username='testuser', full_name=None, title='Sales Executive', education='Undergraduate degree', summary=None, status='Active', employment_type='Full-time', location='Sofia', id=5, skills=['Bussiness Development', 'Marketing', 'Sales', 'Management'])]

        self.assertEqual(result, expected)