from fastapi.testclient import TestClient
from fastapi import HTTPException
from database import get_db
from http import HTTPStatus
from main import app
from unittest import mock
import pytest
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm import Session
from permissions import crud

def override_get_db():
  pass

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture
def permission_data():
    return {
        "id": 1,
        "type_access": "admin"
    }
    
@pytest.fixture   
def mock_session():
  return mock.Mock(spec=Session)   

@mock.patch('permissions.crud.get_permission')
def test_get_permission(mock_get_permission, permission_data):
  """
    Test permissions search route must return success
  """
  permission = [permission_data]

  mock_get_permission.return_value = permission
  response = client.get("/permission")

  assert response.status_code == HTTPStatus.OK
  assert response.json() == permission

@mock.patch('permissions.crud.create_permission')
def test_create_permission(mock_create_permission):
  """
    Test create new permission must return success
  """
  request = "test"

  mock_create_permission.return_value = {"id": 4, "type_access": request}
  response = client.post(f"/permission?type_access={request}")

  assert response.status_code == HTTPStatus.CREATED
  assert response.json() == mock_create_permission.return_value
  
@mock.patch('permissions.crud.create_permission')
def test_create_permission_exists(mock_create_permission):
  """
    Test create new permission but permission exist then return failed
  """
  mock_create_permission.side_effect = HTTPException(
        status_code=HTTPStatus.BAD_REQUEST,
        detail=f"Permission already exists id: 1, type: admin",
    )
  request = "admin"
  response = client.post(f"/permission?type_access={request}")

  assert response.status_code == HTTPStatus.BAD_REQUEST
  assert response.json() == {"detail": "Permission already exists id: 1, type: admin"}
 

def test_get_permission_database_error(mock_session):
    def mock_query(*args, **kwargs):
        raise DatabaseError("Simulating a DatabaseError", statement=None, params=None, orig=None)
    mock_session.query.side_effect = mock_query

    with pytest.raises(HTTPException) as exc_info:
        crud.get_permission(mock_session)
        assert exc_info.value.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
        assert "Database Error" in str(exc_info.value.detail)
        
def test_get_permission_exception_error(mock_session):
    def mock_query(*args, **kwargs):
        raise Exception("Simulating a Exception", statement=None, params=None, orig=None)
    mock_session.query.side_effect = mock_query

    with pytest.raises(HTTPException) as exc_info:
        crud.get_permission(mock_session)
        assert exc_info.value.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
        assert "Internal Server Error" in str(exc_info.value.detail)
        
def test_create_permission_error(mock_session):
  def mock_query(*args, **kwargs):
    raise Exception("Simulating a Exception", statement=None, params=None, orig=None)
  mock_session.query.side_effect = mock_query
  
  with pytest.raises(HTTPException) as exc_info:
    crud.create_permission(mock_session, type_permission="admin")
    assert exc_info.value.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert "Internal Server Error" in str(exc_info.value.detail)


    
   



    


