from http import HTTPStatus
from unittest import TestCase, mock

from fastapi import HTTPException
from fastapi.testclient import TestClient

from auth.utils import verify_token
from database import get_db
from main import app


def override_get_db():...

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)
 
class PermissionTestCase(TestCase):
    def setUp(self):
         self.permission = {
        "id": 1,
        "type_access": "admin"
    }
    def override_verify_token(self):...
    
    @mock.patch("permissions.crud.get_permission")
    def test_get_permission_success(self, mock_get_permission):
        """
            Test permissions search route must return success
        """
        permission = [self.permission, self.permission]
        app.dependency_overrides[verify_token] = self.override_verify_token
        mock_get_permission.return_value = permission
        response = client.get("/permission")

        assert response.status_code == HTTPStatus.OK
        assert response.json() == permission
    
    @mock.patch("permissions.crud.create_permission")
    def test_create_new_permission(self, mock_create_permission):
        """
          Test create new permission must return success
        """
        data = {
            "id": 4,
            "type_access": "admin"
        }
        mock_create_permission.return_value = data
        app.dependency_overrides[verify_token] = self.override_verify_token
        response = client.post("/permission?type_access=admin")
        
        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == data
        
    @mock.patch("permissions.crud.create_permission")
    def test_create_permission_but_exist(self, mock_create_permission):
        """
          Test create permission but permission exist return error
        """
        request = "admin"
        mock_create_permission.side_effect = HTTPException(
        status_code=HTTPStatus.BAD_REQUEST,
         detail=f"Permission already exists id: 1, type: {request}",
     )
       
        response = client.post(f"/permission?type_access={request}")

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == {"detail": "Permission already exists id: 1, type: admin"}