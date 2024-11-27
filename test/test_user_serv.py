import unittest
from unittest.mock import MagicMock
from bcrypt import checkpw
from sqlmodel import Session
from users.user_service import update_user
from data.db_models import User
from utils.auth import get_password_hash

class TestUserService(unittest.TestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user_id = 1
        self.user_update = MagicMock()
        self.user = User(id=self.user_id, username="old_username", password="old_password", first_name="Old", last_name="User", email="old@example.com")

    def test_update_user_success(self):
        self.user_update.username = "new_username"
        self.user_update.new_password = "new_password"
        self.user_update.confirm_password = "new_password"
        self.user_update.first_name = "New"
        self.user_update.last_name = "User"
        self.user_update.email = "new@example.com"

        self.session.exec.return_value.first().return_value = self.user

        updated_user = update_user(self.user_id, self.user_update, self.session)

        self.assertEqual(updated_user.username, "new_username")
        self.assertEqual(checkpw("new_password".encode(), updated_user.password.encode()), True)
        self.assertEqual(updated_user.first_name, "New")
        self.assertEqual(updated_user.last_name, "User")
        self.assertEqual(updated_user.email, "new@example.com")

    def test_update_user_no_user_found(self):
        self.session.exec.return_value.first.return_value = None

        updated_user = update_user(self.user_id, self.user_update, self.session)

        self.assertIsNone(updated_user)

    def test_update_user_password_mismatch(self):
        self.user_update.new_password = "new_password"
        self.user_update.confirm_password = "different_password"

        self.session.exec.return_value.first.return_value = self.user

        with self.assertRaises(ValueError) as context:
            update_user(self.user_id, self.user_update, self.session)

        self.assertEqual(str(context.exception), "New password and confirm password do not match")

