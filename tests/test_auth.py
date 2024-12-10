import unittest
from unittest.mock import patch, MagicMock
from utils.auth import get_current_user, verify_password, authenticate_user
from passlib.context import CryptContext
from sqlmodel import Session
from data.db_models import User
from users import user_service as us
from utils.auth import verify_password, authenticate_user, create_access_token
from datetime import datetime, timedelta
from jose import jwt
from utils.auth import verify_password, authenticate_user, create_access_token, verify_token
from jose import jwt, JWTError
from fastapi import HTTPException

class TestAuthUtils(unittest.TestCase):

    @patch('utils.auth.pwd_context.verify', return_value=True)
    def test_verify_password(self, mock_verify):
        self.assertTrue(verify_password("plain_password", "hashed_password"))
        mock_verify.assert_called_once_with("plain_password", "hashed_password")

    @patch('utils.auth.Session', autospec=True)
    @patch('utils.auth.us.view_user_by_id')
    @patch('utils.auth.select')
    def test_authenticate_user_by_id(self, mock_select, mock_view_user_by_id, mock_session):
        mock_session.return_value.__enter__.return_value = mock_session
        mock_user = MagicMock()
        mock_user.password = "hashed_password"
        mock_view_user_by_id.return_value = mock_user

        with patch('utils.auth.verify_password', return_value=True):
            user = authenticate_user("123", "password")
            self.assertEqual(user, mock_user)
            mock_view_user_by_id.assert_called_once_with(123, mock_session)

    @patch('utils.auth.Session', autospec=True)
    @patch('utils.auth.select')
    def test_authenticate_user_by_username(self, mock_select, mock_session):
        mock_session.return_value.__enter__.return_value = mock_session
        mock_user = MagicMock()
        mock_user.password = "hashed_password"
        mock_session.exec.return_value.first.return_value = mock_user

        with patch('utils.auth.verify_password', return_value=True):
            user = authenticate_user("username", "password")
            self.assertEqual(user, mock_user)
            mock_select.assert_called_once()
            mock_session.exec.assert_called_once()

    @patch('utils.auth.Session', autospec=True)
    @patch('utils.auth.us.view_user_by_id')
    def test_authenticate_user_not_found(self, mock_view_user_by_id, mock_session):
        mock_session.return_value.__enter__.return_value = mock_session
        mock_view_user_by_id.return_value = None

        user = authenticate_user("123", "password")
        self.assertIsNone(user)
        mock_view_user_by_id.assert_called_once_with(123, mock_session)

    @patch('utils.auth.Session', autospec=True)
    @patch('utils.auth.select')
    def test_authenticate_user_incorrect_password(self, mock_select, mock_session):
        mock_session.return_value.__enter__.return_value = mock_session
        mock_user = MagicMock()
        mock_user.password = "hashed_password"
        mock_session.exec.return_value.first.return_value = mock_user

        with patch('utils.auth.verify_password', return_value=False):
            user = authenticate_user("username", "password")
            self.assertIsNone(user)
            mock_select.assert_called_once()
            mock_session.exec.assert_called_once()
           
    @patch('utils.auth.jwt.encode')
    @patch('utils.auth.datetime')
    @patch('utils.auth.key', 'test_key')
    @patch('utils.auth.algorithm', 'HS256')
    @patch('utils.auth.access_token_expire_minutes', 30)
    def test_create_access_token(self, mock_datetime, mock_jwt_encode):
        mock_datetime.now.return_value = datetime(2023, 1, 1)
        mock_jwt_encode.return_value = 'test_token'
        data = {"sub": "test_user"}
        token = create_access_token(data)
        self.assertEqual(token, 'test_token')
        mock_jwt_encode.assert_called_once_with(
            {"sub": "test_user", "exp": datetime(2023, 1, 1) + timedelta(minutes=30)},
            'test_key',
            algorithm='HS256'
        )
       

    @patch('utils.auth.jwt.decode')
    @patch('utils.auth.key', 'test_key')
    @patch('utils.auth.algorithm', 'HS256')
    def test_verify_token_valid(self, mock_jwt_decode):
        mock_jwt_decode.return_value = {'sub': 'test_user'}
        token = 'valid_token'
        payload = verify_token(token)
        self.assertEqual(payload, {'sub': 'test_user'})
        mock_jwt_decode.assert_called_once_with(token, 'test_key', algorithms=['HS256'])

    @patch('utils.auth.jwt.decode', side_effect=JWTError)
    @patch('utils.auth.key', 'test_key')
    @patch('utils.auth.algorithm', 'HS256')
    def test_verify_token_invalid(self, mock_jwt_decode):
        token = 'invalid_token'
        payload = verify_token(token)
        self.assertIsNone(payload)
        mock_jwt_decode.assert_called_once_with(token, 'test_key', algorithms=['HS256'])

    def test_verify_token_revoked(self):
        token = 'revoked_token'
        with patch('utils.auth.token_blacklist', {token}):
            with self.assertRaises(HTTPException):
                verify_token(token)

    def test_verify_token_empty(self):
        token = ''
        payload = verify_token(token)
        self.assertIsNone(payload)


    @patch('utils.auth.Session', autospec=True)
    @patch('utils.auth.us.get_user')
    @patch('utils.auth.verify_token')
    def test_get_current_user_valid_token(self, mock_verify_token, mock_get_user, mock_session):
        mock_session.return_value.__enter__.return_value = mock_session
        mock_verify_token.return_value = {'sub': 'test_user', 'user_id': 1}
        mock_user = MagicMock()
        mock_get_user.return_value = mock_user

        token = 'valid_token'
        user = get_current_user(token)
        self.assertEqual(user, mock_user)
        mock_verify_token.assert_called_once_with(token)
        mock_get_user.assert_called_once_with('test_user', 1, session=mock_session.return_value)

    @patch('utils.auth.verify_token', return_value=None)
    def test_get_current_user_invalid_token(self, mock_verify_token):
        token = 'invalid_token'
        user = get_current_user(token)
        self.assertIsNone(user)
        mock_verify_token.assert_called_once_with(token)

    @patch('utils.auth.verify_token')
    def test_get_current_user_no_username(self, mock_verify_token):
        mock_verify_token.return_value = {'user_id': 1}
        token = 'valid_token'
        user = get_current_user(token)
        self.assertIsNone(user)
        mock_verify_token.assert_called_once_with(token)

    @patch('utils.auth.verify_token')
    def test_get_current_user_no_user_id(self, mock_verify_token):
        mock_verify_token.return_value = {'sub': 'test_user'}
        token = 'valid_token'
        user = get_current_user(token)
        self.assertIsNone(user)
        mock_verify_token.assert_called_once_with(token)

    def test_get_current_user_no_token(self):
        token = None
        user = get_current_user(token)
        self.assertIsNone(user)


       




