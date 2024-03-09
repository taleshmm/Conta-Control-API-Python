from http import HTTPStatus
from unittest import TestCase, mock

from fastapi.testclient import TestClient

from auth.utils import verify_token
from database import get_db
from main import app


class AuthTestCase(TestCase):
    def setUp(self):
        ...
        
    # @mock.patch("users.crud.create_user")
    # def test_create_new_permission(self, mock_create_user):
    #     """
    #       Test create new user must return success
    #     """
    #     request = self.user_request
    #     mock_create_user.return_value = request
    #     app.dependency_overrides[verify_token] = self.override_verify_token
    #     response = client.post("/user", json=request)
        
    #     user_response = CreateUserResponse(**request)
        
    #     assert response.status_code == HTTPStatus.CREATED
    #     assert response.json() == user_response.__dict__.copy()
     
    # @mock.patch("users.crud.get_user_email")   
    # @mock.patch("users.crud.create_user")
    # def test_create_permission_but_exist(self, mock_create_user, mock_get_user_email):
    #     """
    #       Test create user but user exist return error
    #     """
    #     request = self.user_request
    #     mock_get_user_email.return_value = self.user_instance
    #     error_message = f"User already exists email: {request['email']}"
    #     mock_create_user.side_effect = HTTPException(
    #     status_code=HTTPStatus.BAD_REQUEST,
    #      detail=error_message,
    #  )
       
    #     response = client.post(f"/user", json=request)

    #     assert response.status_code == HTTPStatus.BAD_REQUEST
    #     assert response.json() == {"detail": error_message}
    