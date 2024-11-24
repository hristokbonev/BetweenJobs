import unittest
from fastapi import HTTPException
from utils.auth import create_access_token, get_current_user, get_password_hash, verify_password, authenticate_user, verify_token
from unittest.mock import patch, MagicMock
from sqlmodel import Session
from utils.crud import get_user_by_username
from datetime import datetime, timedelta
from jose import JWTError, jwt
from utils.auth import key, algorithm, access_token_expire_minutes, token_blacklist




class TestAuthUtilsPassword(unittest.TestCase):

    def test_get_password_hash(self):
        password = "mysecretpassword"
        hashed_password = get_password_hash(password)
        self.assertNotEqual(password, hashed_password)
        self.assertTrue(hashed_password.startswith("$2b$"))

    def test_verify_password(self):
        password = "mysecretpassword"
        hashed_password = get_password_hash(password)
        self.assertTrue(verify_password(password, hashed_password))
        self.assertFalse(verify_password("wrongpassword", hashed_password))

    @patch('utils.auth.Session', autospec=True)
    @patch('utils.auth.get_user_by_username', autospec=True)
    def test_authenticate_user(self, mock_get_user_by_username, mock_session):
        username = "testuser"
        password = "testpassword"
        hashed_password = get_password_hash(password)

        mock_user = MagicMock()
        mock_user.password = hashed_password
        mock_get_user_by_username.return_value = mock_user

        with mock_session() as session:
            user = authenticate_user(username, password)
            self.assertIsNotNone(user)
            self.assertEqual(user, mock_user)

            mock_get_user_by_username.return_value = None
            user = authenticate_user(username, password)
            self.assertIsNone(user)

            mock_get_user_by_username.return_value = mock_user
            user = authenticate_user(username, "wrongpassword")
            self.assertIsNone(user)
 
 
class TestAuthUtils(unittest.TestCase):

    # ... existing tests ...

    @patch('utils.auth.datetime', autospec=True)
    @patch('utils.auth.jwt.encode', autospec=True)
    def test_create_access_token(self, mock_jwt_encode, mock_datetime):
        data = {"sub": "testuser"}
        mock_datetime.now.return_value = datetime(2023, 1, 1)
        mock_jwt_encode.return_value = "testtoken"

        token = create_access_token(data)
        self.assertEqual(token, "testtoken")

        expected_exp = mock_datetime.now() + timedelta(minutes=int(access_token_expire_minutes))
        mock_jwt_encode.assert_called_once_with(
            {"sub": "testuser", "exp": expected_exp},
            key,
            algorithm=algorithm
        )


class TestAuthUtils(unittest.TestCase):

    # ... existing tests ...

    @patch('utils.auth.jwt.decode', autospec=True)
    def test_verify_token_valid(self, mock_jwt_decode):
        token = "validtoken"
        mock_jwt_decode.return_value = {"sub": "testuser"}

        payload = verify_token(token)
        self.assertIsNotNone(payload)
        self.assertEqual(payload.get('sub'), "testuser")

    @patch('utils.auth.jwt.decode', autospec=True)
    def test_verify_token_invalid(self, mock_jwt_decode):
        token = "invalidtoken"
        mock_jwt_decode.side_effect = JWTError

        payload = verify_token(token)
        self.assertIsNone(payload)

    def test_verify_token_revoked(self):
        token = "revokedtoken"
        token_blacklist.add(token)

        with self.assertRaises(HTTPException) as context:
            verify_token(token)
        self.assertEqual(context.exception.status_code, 401)
        self.assertEqual(context.exception.detail, "Token has been revoked")

    def test_verify_token_empty(self):
        token = ""

        payload = verify_token(token)
        self.assertIsNone(payload)

        
class TestAuthUtils(unittest.TestCase):

    # ... existing tests ...

    @patch('utils.auth.verify_token', autospec=True)
    @patch('utils.auth.get_user', autospec=True)
    @patch('utils.auth.Session', autospec=True)
    def test_get_current_user_valid(self, mock_session, mock_get_user, mock_verify_token):
        token = "validtoken"
        mock_verify_token.return_value = {"sub": "testuser"}
        mock_user = MagicMock()
        mock_get_user.return_value = mock_user

        with patch('utils.auth.Depends', return_value=token):
            user = get_current_user(token)
            self.assertIsNotNone(user)
            self.assertEqual(user, mock_user)

    @patch('utils.auth.verify_token', autospec=True)
    def test_get_current_user_invalid_token(self, mock_verify_token):
        token = "invalidtoken"
        mock_verify_token.return_value = None

        with patch('utils.auth.Depends', return_value=token):
            user = get_current_user(token)
            self.assertIsNone(user)

    @patch('utils.auth.verify_token', autospec=True)
    def test_get_current_user_no_username(self, mock_verify_token):
        token = "validtoken"
        mock_verify_token.return_value = {}

        with patch('utils.auth.Depends', return_value=token):
            user = get_current_user(token)
            self.assertIsNone(user)

    def test_get_current_user_no_token(self):
        token = None

        with patch('utils.auth.Depends', return_value=token):
            user = get_current_user(token)
            self.assertIsNone(user)


