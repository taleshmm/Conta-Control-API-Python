from fastapi.testclient import TestClient
from database import get_db, models
from http import HTTPStatus
from main import app
from unittest import mock
from pytest import fixture
from response import UserResponse


def override_get_db():
  pass

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@fixture
def user_response_fixture():
  type_access_data = {
    "id": 2,
    "type_access": "standard"
}
  type_access_instance = models.Permission  (**type_access_data)
  user_data = {
    "id": 1,
    "email": "teste@icloud.com",
    "name": "João Silva",
    "nickname": "João",
    "sex": "M",
    "hashed_password": 'senha',
    "type_access": type_access_instance
}
  user_instance = models.User(**user_data)
  return user_instance

@fixture
def user_data_fixture():
  user_data = UserResponse(id=1, email="teste@icloud.com", name="João Silva", nickname="João", sex="M", type_access="premium")
  return user_data

# 
@mock.patch('users.crud.get_user_email')
def test_get_user_by_email(mock_get_user, user_response_fixture):
    """
    Test to search for user by email must return success
    """
    request = "teste@icloud.com"

    mock_get_user.return_value = user_response_fixture
    response = client.get(f"user/email?email={request}")
    
    user_response_fixture_dict = user_response_fixture.__dict__.copy()       
    user_response_fixture_dict['type_access'] = user_response_fixture.type_access.type_access  
    user_response = UserResponse(**user_response_fixture_dict)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_response.__dict__.copy()
    
@mock.patch('users.crud.get_users')
def test_get_users(mock_get_user, user_data_fixture):
  """
    Test to search for all users must return success
  """
  mock_get_user.return_value = [user_data_fixture]
  skip = 0
  limit = 10
  response = client.get(f"user?skip={skip}&limit={limit}")
  expected_user_data = [user_data_fixture.__dict__.copy()]  

  assert response.status_code == HTTPStatus.OK
  assert response.json() == expected_user_data
  
@mock.patch('users.crud.create_user')
def test_create_user(mock_create_user):
  """
  Teste created user must return success
  """
  user_create_return = {
    "id": 10,
    "email": "teste@gmail.com",
    "name": "Vi Duarte"
  }
  
  user_create_data = {
    "email": "teste@gmail.com",
    "name": "Vi Duarte",
    "nickname": "Vivi",
    "sex": "F",
    "password": 'senha',
    "type_access": 2
  }
  mock_create_user.return_value = user_create_return
  response = client.post("user", json=user_create_data)
  
  assert response.status_code == HTTPStatus.CREATED
  assert response.json() == user_create_return
  
