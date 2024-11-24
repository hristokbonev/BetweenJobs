from datetime import date
import unittest
from unittest.mock import MagicMock, patch
from sqlmodel import Session
from data.db_models import User
from users.user_models import UserCreate, UserModel
from utils.authentication import create_user
from utils.crud import get_user, get_user_by_username



class TestCrudFunctions(unittest.TestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.username = "testuser"
        self.user_data = {
            "username": self.username,
            "password": "password123",
            "first_name": "Test",
            "last_name": "User",
            "is_admin": False,
            "date_of_birth": None,
            "email": "testuser@example.com"
        }
        self.user = User(**self.user_data)

    def test_get_user(self):
        self.session.exec.return_value.first.return_value = self.user
        result = get_user(self.username, self.session)
        self.assertIsInstance(result, UserModel)
        self.assertEqual(result.username, self.username)

    def test_get_user_not_found(self):
        self.session.exec.return_value.first.return_value = None
        result = get_user(self.username, self.session)
        self.assertIsNone(result)

    def test_get_user_by_username(self):
        self.session.exec.return_value.first.return_value = self.user
        result = get_user_by_username(self.session, self.username)
        self.assertIsInstance(result, User)
        self.assertEqual(result.username, self.username)

    def test_get_user_by_username_not_found(self):
        self.session.exec.return_value.first.return_value = None
        result = get_user_by_username(self.session, self.username)
        self.assertIsNone(result)



