import unittest
from users.user_service import get_password_hash, user_has_companies, create_new_skill, view_users, view_user_by_id, get_filtered_users, update_user, get_user
from passlib.context import CryptContext
from unittest.mock import MagicMock
from sqlmodel import Session
from data.db_models import User, Variables
from users.user_models import UserSearch, UserUpdate, UserModel, TestModeResponse, UserCreate
from users.user_service import get_password_hash, view_users, view_user_by_id, create_new_skill
from data.db_models import User, Skill
from users.user_models import CreateSkillRequest
from users.user_models import CreateSkillRequest
from data.db_models import Skill
from users.user_service import (
    get_password_hash, view_users, view_user_by_id, 
    get_filtered_users, update_user, swith_test_mode, get_user
)


class TestUserService(unittest.TestCase):

    def setUp(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.session = MagicMock(spec=Session)

    def test_get_password_hash(self):
        password = "mysecretpassword"
        hashed_password = get_password_hash(password)
        
        self.assertIsNotNone(hashed_password)
        self.assertNotEqual(password, hashed_password)
        self.assertTrue(self.pwd_context.verify(password, hashed_password))

    def test_view_users(self):
        mock_users = [User(id=1, username="user1"), User(id=2, username="user2")]
        self.session.exec.return_value.all.return_value = mock_users

        users = view_users(self.session)

        self.assertEqual(users, mock_users)
        self.session.exec.assert_called_once()

    def test_view_user_by_id(self):
        mock_user = User(id=1, username="user1")
        self.session.exec.return_value.first.return_value = mock_user

        user = view_user_by_id(1, self.session)

        self.assertEqual(user, mock_user)
        self.session.exec.assert_called_once()

    def test_get_filtered_users(self):
        search_criteria = UserSearch(username="user")
        mock_users = [User(id=1, username="user1"), User(id=2, username="user2")]
        self.session.exec.return_value.all.return_value = mock_users

        users = get_filtered_users(search_criteria, 1, 10, self.session)

        self.assertEqual(users, mock_users)
        self.session.exec.assert_called_once()

    def test_update_user(self):
        user_update = UserUpdate(username="newuser", new_password="newpass", confirm_password="newpass")
        mock_user = User(id=1, username="olduser")
        self.session.exec.return_value.first.return_value = mock_user

        updated_user = update_user(1, user_update, self.session)

        self.assertEqual(updated_user.username, "newuser")
        self.assertTrue(self.pwd_context.verify("newpass", updated_user.password))
        self.session.commit.assert_called_once()
        self.session.refresh.assert_called_once()

    def test_update_user_password_mismatch(self):
        user_update = UserUpdate(username="newuser", new_password="newpass", confirm_password="wrongpass")
        mock_user = User(id=1, username="olduser")
        self.session.exec.return_value.first.return_value = mock_user

        with self.assertRaises(ValueError):
            update_user(1, user_update, self.session)

    def test_swith_test_mode(self):
        mock_status = Variables(var_id=1, email_test_mode=0)
        self.session.exec.return_value.first.return_value = mock_status
        
        response = swith_test_mode(self.session, UserModel(
            id=1, 
            username="admin", 
            first_name="Test", 
            last_name="User", 
            email="admin@example.com"
        ))

    def test_get_user(self):
        mock_user = User(
            id=1, 
            username="user1", 
            first_name="Test", 
            last_name="User",   
            email="test@example.com" 
        )
        
        self.session.exec.return_value.first.return_value = mock_user
        
        user = get_user("user1", 1, self.session)
        
        self.assertEqual(user.username, "user1")
        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "User")
        self.assertEqual(user.email, "test@example.com")


    def test_get_filtered_users_username(self):
        search_criteria = UserSearch(username="user")
        mock_users = [User(id=1, username="user1"), User(id=2, username="user2")]
        self.session.exec.return_value.all.return_value = mock_users

        users = get_filtered_users(search_criteria, 1, 10, self.session)

        self.assertEqual(users, mock_users)
        self.session.exec.assert_called_once()

    def test_get_filtered_users_first_name(self):
        search_criteria = UserSearch(first_name="Test")
        mock_users = [User(id=1, first_name="Test1"), User(id=2, first_name="Test2")]
        self.session.exec.return_value.all.return_value = mock_users

        users = get_filtered_users(search_criteria, 1, 10, self.session)

        self.assertEqual(users, mock_users)
        self.session.exec.assert_called_once()

    def test_get_filtered_users_last_name(self):
        search_criteria = UserSearch(last_name="User")
        mock_users = [User(id=1, last_name="User1"), User(id=2, last_name="User2")]
        self.session.exec.return_value.all.return_value = mock_users

        users = get_filtered_users(search_criteria, 1, 10, self.session)

        self.assertEqual(users, mock_users)
        self.session.exec.assert_called_once()

    def test_get_filtered_users_email(self):
        search_criteria = UserSearch(email="test@example.com")
        mock_users = [User(id=1, email="test1@example.com"), User(id=2, email="test2@example.com")]
        self.session.exec.return_value.all.return_value = mock_users

        users = get_filtered_users(search_criteria, 1, 10, self.session)

        self.assertEqual(users, mock_users)
        self.session.exec.assert_called_once()

    def test_get_filtered_users_pagination(self):
        search_criteria = UserSearch(username="user")
        mock_users = [User(id=1, username="user1"), User(id=2, username="user2")]
        self.session.exec.return_value.all.return_value = mock_users

        users = get_filtered_users(search_criteria, 2, 1, self.session)

        self.assertEqual(users, mock_users)
        self.session.exec.assert_called_once()
        

    def test_update_user(self):
        user_update = UserUpdate(username="newuser2", new_password="newpass2", confirm_password="newpass2")
        mock_user = User(id=3, username="olduser1")
        self.session.exec.return_value.first.return_value = mock_user

        updated_user = update_user(1, user_update, self.session)

        self.assertEqual(updated_user.username, "newuser2")
        self.assertTrue(self.pwd_context.verify("newpass2", updated_user.password))
        self.session.commit.assert_called_once()
        self.session.refresh.assert_called_once()

    def test_update_user_password_mismatch(self):
        user_update = UserUpdate(username="newuser2", new_password="newpass2", confirm_password="wrongpass")
        mock_user = User(id=1, username="olduser1")
        self.session.exec.return_value.first.return_value = mock_user

        with self.assertRaises(ValueError):
            update_user(1, user_update, self.session)

    def test_update_user_not_found(self):
        user_update = UserUpdate(username="newuser2", new_password="newpass2", confirm_password="newpass2")
        self.session.exec.return_value.first.return_value = None

        updated_user = update_user(1, user_update, self.session)

        self.assertIsNone(updated_user)
        self.session.commit.assert_not_called()
        self.session.refresh.assert_not_called()


    def test_user_has_companies_true(self):
        mock_user = User(id=1, username="user1")
        self.session.exec.return_value.first.return_value = mock_user

        has_companies = user_has_companies(1, self.session)

        self.assertTrue(has_companies)
        self.session.exec.assert_called_once()

    def test_user_has_companies_false(self):
        self.session.exec.return_value.first.return_value = None

        has_companies = user_has_companies(1, self.session)

        self.assertFalse(has_companies)
        self.session.exec.assert_called_once()
        

    def test_switch_test_mode_enable(self):
        mock_status = Variables(var_id=1, email_test_mode=0)
        self.session.exec.return_value.first.return_value = mock_status

        response = swith_test_mode(self.session, UserModel(
            id=1, 
            username="admin", 
            first_name="Test", 
            last_name="User", 
            email="admin@example.com"
        ))

        self.assertEqual(response.status, 1)
        self.session.add.assert_called_once_with(mock_status)
        self.session.commit.assert_called_once()
        self.session.refresh.assert_called_once_with(mock_status)

    def test_switch_test_mode_disable(self):
        mock_status = Variables(var_id=1, email_test_mode=1)
        self.session.exec.return_value.first.return_value = mock_status

        response = swith_test_mode(self.session, UserModel(
            id=1, 
            username="admin", 
            first_name="Test", 
            last_name="User", 
            email="admin@example.com"
        ))

        self.assertEqual(response.status, 0)
        self.session.add.assert_called_once_with(mock_status)
        self.session.commit.assert_called_once()
        self.session.refresh.assert_called_once_with(mock_status)
        

    def test_create_new_skill_success(self):
        data = CreateSkillRequest(name="Python")
        mock_skill = Skill(id=1, name="Python")

    
        scalars_mock = MagicMock()
        scalars_mock.first.side_effect = [None, mock_skill]
        self.session.execute.return_value.scalars.return_value = scalars_mock

        new_skill = create_new_skill(data, self.session)

        self.assertEqual(new_skill.name, "Python")

        