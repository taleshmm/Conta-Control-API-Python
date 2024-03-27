from http import HTTPStatus
from unittest import TestCase, mock

import jwt
from fastapi.testclient import TestClient

from auth import schemas
from auth.utils import ALGORITHM, SECRET_KEY, verify_token
from database import get_db
from main import app


def override_get_db():...

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)
class AuthTestCase(TestCase):
    def setUp(self):
        self.user_auth = {
            "email": "john@doe.com",
            "password": "12345"           
        }
        self.user_authentication = schemas.UserAuthentication(**self.user_auth)
        self.token = jwt.encode({"email": "john@doe.com"}, SECRET_KEY, algorithm=ALGORITHM)
        self.user_data = {
            "id": 1,
            "email": "john@doe.com",
            "name": "John Doe",
            "nickname": "JD",
            "sex": "M",
            "type_access": 2
        }
        self.user_auth_sing = {
            "email": "john@doe.com",
            "password": "12345",
            "confirm_password": "12345",
            "name": "John Doe",
            "nickname": "JD",
            "sex": "M",
            "type_access": 2
        }
        
    @mock.patch("auth.utils.validate_user")
    @mock.patch("auth.utils.jwt.encode")
    def test_create_token(self, mock_encode, mock_validate_user):
        mock_validate_user.return_value = self.user_data
        mock_encode.return_value = "mocked_token"

        response = client.post("/auth/login", json=self.user_auth)
        data = response.json()

        assert response.status_code == HTTPStatus.OK
        assert "token" in data
        assert "exp" in data

        mock_encode.assert_called_once_with(
            {"email": self.user_auth["email"], "exp": mock.ANY},
            SECRET_KEY,
            ALGORITHM
        )
        
    @mock.patch("auth.utils.create_token")
    @mock.patch("auth.crud.create_user")
    def test_signup(self, mock_create_user, mock_create_token):
        mock_create_user.return_value = self.user_data
        mock_create_token.return_value = "mocked_token"

        response = client.post("/auth/signup", json=self.user_auth_sing)
        data = response.json()

        assert response.status_code == HTTPStatus.OK
        assert "user" in data
        assert data["user"] == self.user_data
        assert "token" in data
        assert data["token"] == "mocked_token"
        