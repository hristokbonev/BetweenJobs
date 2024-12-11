import unittest
from unittest.mock import MagicMock
from sqlmodel import Session
from utils.attribute_service import education_exists, get_all_employments, get_all_locations, get_distinct_column_values, get_employment_type_by_id, get_skill_by_id, get_skills_for_job, location_exists, skill_exists, status_exists, view_education_by_id, get_employment_by_id, get_location_by_id, get_status_by_id
from data.db_models import Education, EmploymentType, Location, Status
from data.db_models import Education, EmploymentType, Location, Status, Skill, JobAdSkill

class TestAttributeService(unittest.TestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)

    def test_view_education_by_id(self):
        education_id = 1
        expected_degree_level = "Bachelor's"
        self.session.exec.return_value.first.return_value = expected_degree_level

        result = view_education_by_id(education_id, self.session)
        self.session.exec.assert_called_once()
        self.assertEqual(result, expected_degree_level)

    def test_get_employment_by_id(self):
        employment_id = 1
        expected_employment_name = "Full-time"
        self.session.exec.return_value.first.return_value = expected_employment_name

        result = get_employment_by_id(employment_id, self.session)
        self.session.exec.assert_called_once()
        self.assertEqual(result, expected_employment_name)

    def test_get_location_by_id(self):
        location_id = 1
        expected_location_name = "New York"
        self.session.exec.return_value.first.return_value = expected_location_name

        result = get_location_by_id(location_id, self.session)
        self.session.exec.assert_called_once()
        self.assertEqual(result, expected_location_name)

    def test_get_status_by_id(self):
        status_id = 1
        expected_status_name = "Active"
        self.session.exec.return_value.first.return_value = expected_status_name

        result = get_status_by_id(status_id, self.session)
        self.session.exec.assert_called_once()
        self.assertEqual(result, expected_status_name)


    def test_get_skill_by_id(self):
        skill_id = 1
        expected_skill = Skill(id=skill_id, name="Python")
        self.session.exec.return_value.first.return_value = expected_skill

        result = get_skill_by_id(skill_id, self.session)
        self.session.exec.assert_called_once()
        self.assertEqual(result, expected_skill)

    def test_get_skills_for_job(self):
        job_id = 1
        skill_ids = [1, 2]
        expected_skills = [Skill(id=1, name="Python"), Skill(id=2, name="Django")]
        self.session.exec.return_value.all.return_value = skill_ids

        self.session.exec.side_effect = [
            MagicMock(all=MagicMock(return_value=skill_ids)),
            MagicMock(first=MagicMock(return_value=expected_skills[0])),
            MagicMock(first=MagicMock(return_value=expected_skills[1]))
        ]

        result = get_skills_for_job(job_id, self.session)
        self.assertEqual(result, expected_skills)

    def test_get_distinct_column_values(self):
        column = Education.degree_level
        expected_values = ["Bachelor's", "Master's"]
        self.session.exec.return_value.all.return_value = [(value,) for value in expected_values]

        result = get_distinct_column_values(self.session, column)
        self.session.exec.assert_called_once()
        self.assertEqual(result, expected_values)

    def test_education_exists(self):
        education = "Bachelor's"
        self.session.exec.return_value.first.return_value = 1

        result = education_exists(education, self.session)
        self.session.exec.assert_called_once()
        self.assertTrue(result)
        

    def test_get_employment_type_by_id(self):
        employment_id = 1
        expected_employment_name = "Full-time"
        self.session.exec.return_value.first.return_value = expected_employment_name

        result = get_employment_type_by_id(employment_id, self.session)
        self.session.exec.assert_called_once()
        self.assertEqual(result, expected_employment_name)

    def test_get_all_locations(self):
        expected_locations = ["New York", "San Francisco"]
        self.session.exec.return_value.all.return_value = expected_locations

        result = get_all_locations(self.session)
        self.session.exec.assert_called_once()
        self.assertEqual(result, expected_locations)

    def test_get_all_employments(self):
        expected_employments = ["Full-time", "Part-time"]
        self.session.exec.return_value.all.return_value = expected_employments

        result = get_all_employments(self.session)
        self.session.exec.assert_called_once()
        self.assertEqual(result, expected_employments)

    def test_location_exists(self):
        location = "New York"
        self.session.exec.return_value.first.return_value = 1

        result = location_exists(location, self.session)
        self.session.exec.assert_called_once()
        self.assertTrue(result)

    def test_skill_exists(self):
        skill = "Python"
        self.session.exec.return_value.first.return_value = 1

        result = skill_exists(skill, self.session)
        self.session.exec.assert_called_once()
        self.assertTrue(result)

    def test_status_exists(self):
        status = "Active"
        self.session.exec.return_value.first.return_value = 1

        result = status_exists(status, self.session)
        self.session.exec.assert_called_once()
        self.assertTrue(result)



