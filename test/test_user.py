from http import HTTPStatus
from unittest import TestCase, mock

from fastapi import HTTPException
from fastapi.testclient import TestClient

from auth.utils import verify_token
from database import get_db, models
from main import app
from response import CreateUserResponse, UserResponse


def override_get_db():...

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)
 
class UserTestCase(TestCase):
    def setUp(self):
        self.type_access_data = {
            "id": 1,
            "type_access": "admin"
        }
        self.type_access_instance = models.Permission(**self.type_access_data)
        self.user_data = {
            "id": 1,
            "email": "teste@icloud.com",
            "name": "João Silva",
            "nickname": "João",
            "sex": "M",
            "hashed_password": '1234',
            "type_access": self.type_access_instance
        }
        self.user_instance = models.User(**self.user_data)
        self.user_request = {
            "id": 1,
            "email": "teste@icloud.com",
            "name": "João Silva",
            "nickname": "João",
            "sex": "M",
            "password": '1234',
            "type_access": 1 
        }
        
    def override_verify_token(self):...
    
    def get_user_response(self):
        """
            Get a user response for testing.
         """
        user_response_fixture_dict = self.user_instance.__dict__.copy()       
        user_response_fixture_dict['type_access'] = self.user_instance.type_access.type_access  
        user_response = UserResponse(**user_response_fixture_dict)
        return user_response
    
    @mock.patch("users.crud.get_user_email")
    def test_get_user_email_success(self, mock_get_user_email):
        """
            Test successful retrieval of user by email.
        """
        app.dependency_overrides[verify_token] = self.override_verify_token
        fake_email = 'test@example.com'
        mock_get_user_email.return_value = self.user_instance

        response = client.get(f"/user/email?email={fake_email}")
        
        assert response.status_code == HTTPStatus.OK
        assert response.json() == self.get_user_response().__dict__.copy()
        
    @mock.patch("users.crud.get_user_by_id")
    def test_get_user_by_id(self, mock_get_user_by_id):
        """
            Test to search for user by id must return success
        """
        app.dependency_overrides[verify_token] = self.override_verify_token
        fake_id = 2
        mock_get_user_by_id.return_value = self.user_instance

        response = client.get(f"/user/id?id={fake_id}")
     
        assert response.status_code == HTTPStatus.OK
        assert response.json() == self.get_user_response().__dict__.copy() 
        
        
    @mock.patch("users.crud.get_users")
    def test_get_users(self, mock_get_users):
        """
            Test to search for all users must return success
        """
        app.dependency_overrides[verify_token] = self.override_verify_token
        
        mock_get_users.return_value = [self.get_user_response()]
        skip = 0
        limit = 10
        response = client.get(f"user?skip={skip}&limit={limit}")
        
        assert response.status_code == HTTPStatus.OK
        assert response.json() == [dict(self.get_user_response())]
    
    @mock.patch("users.crud.delete_user_db")
    @mock.patch("users.crud.get_user_email")
    def test_delete_user_success(self, mock_get_user_email, mock_delete_user_db):
        """
            Test successful deleted user.
        """
        app.dependency_overrides[verify_token] = self.override_verify_token
        fake_email = 'test@example.com'
        mock_get_user_email.return_value = models.User(email=fake_email)
        mock_delete_user_db.return_value = fake_email

        response = client.delete(f"/user?email={fake_email}")
        
        assert response.status_code == HTTPStatus.OK
        assert response.json() == f"User {fake_email} deleted with success."
        
    @mock.patch("users.crud.get_user_by_id")
    @mock.patch("users.crud.updated_user")
    def test_update_user_success(self, mock_updated_user, mock_get_user_by_id):
        """
            Test successful update user.
        """
        app.dependency_overrides[verify_token] = self.override_verify_token
        fake_user_id = 1
        user_data = self.user_request
    
        mock_get_user_by_id.return_value = user_data
   
        updated_user_data = {
        'id': user_data['id'],
        'name': 'J Silva M',
        'nickname': user_data['nickname'],
        'sex': user_data['sex'],
        'email': user_data['email'],
        'password': user_data['password'],
        'type_access': user_data['type_access']
    }
        mock_updated_user.return_value = {'message': 'User updated successfully', 'user': updated_user_data}
        response = client.put("/user", json=user_data)

        assert response.status_code == HTTPStatus.OK
        assert response.json() == {
            'message': 'User updated successfully',
            'user': updated_user_data
        }