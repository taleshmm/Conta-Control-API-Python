from datetime import date
from http import HTTPStatus
from unittest import TestCase, mock

from fastapi import HTTPException
from fastapi.testclient import TestClient

from accounts import schemas
from auth.utils import verify_token
from database import get_db
from main import app


def override_get_db():...

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)
 
class AccountTestCase(TestCase):
    def setUp(self):
        self.account_data = {
            "id": 1,
            "id_user": 298,
            "type_account": "services",
            "name_account": "Energy",
            "value_total": 80.90,
            "installments": 0,
            "value_installments": 0,
            "date_buy": str(date.today()) }
        
        self.create_account_data = {
            "id_user": 298,
            "type_account": "services",
            "name_account": "Energy",
            "value_total": 80.90,
            "installments": 0,
            "value_installments": 0,
            "date_buy": str(date.today())}
        
        self.account_model = schemas.AccountModel(**self.account_data)
        self.account_request = schemas.AccountRequest(**self.account_data)
        self.account_create = schemas.CreateAccount(**self.create_account_data)
        self.account_update = schemas.UpdateAccount(**self.account_data)
        self.user = {
            "id": 298,
            "email": "teste@icloud.com",
            "name": "João Silva",
            "nickname": "João",
            "sex": "M",
            "type_access": 1 
        }
    
           
    def override_verify_token(self):...
    
    @mock.patch("accounts.crud.get_read_all_accounts")
    def test_read_all_accounts(self, mock_get_read_all_accounts):
        app.dependency_overrides[verify_token] = self.override_verify_token
        mock_get_read_all_accounts.return_value = [self.account_model]
        skip = 0
        limit = 10
        faker_id = 298

        response = client.get(f"/account?id_user={faker_id}&skip={skip}&limit={limit}")
        expected_data = self.account_model.__dict__.copy()
        expected_data["date_buy"] = str(expected_data["date_buy"])
        
        assert response.status_code == HTTPStatus.OK
        assert response.json() == [expected_data]

    @mock.patch("accounts.crud.get_read_unique_account")
    def test_read_unique_account(self, mock_get_read_unique_account):
        app.dependency_overrides[verify_token] = self.override_verify_token
       
        mock_get_read_unique_account.return_value = self.account_request
        response = client.get("/account/id?id_user=298&id_account=1")
        
        expected_data = self.account_request.__dict__.copy()
        expected_data["date_buy"] = str(expected_data["date_buy"])
        
        assert response.status_code == HTTPStatus.OK
        assert response.json() == expected_data

    @mock.patch("accounts.crud.create_account")
    def test_create_account(self, mock_create_account):
        app.dependency_overrides[verify_token] = self.override_verify_token
        mock_create_account.return_value = self.account_create
        
        response = client.post("/account", json=self.create_account_data)
        
        expected_data = self.account_create.__dict__.copy()
        expected_data["date_buy"] = str(expected_data["date_buy"])
        
        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == expected_data

    @mock.patch("accounts.crud.update_account")
    def test_update_account(self, mock_update_account):
        app.dependency_overrides[verify_token] = self.override_verify_token
        mock_update_account.return_value = self.account_update
        response = client.put("/account?id_user=298", json=self.account_data)
        expected_data = self.account_update.__dict__.copy()
        expected_data["date_buy"] = str(expected_data["date_buy"])
        
        assert response.status_code == HTTPStatus.OK
        assert response.json() == expected_data

    @mock.patch("accounts.crud.delete_account")
    def test_delete_account(self, mock_delete_account):
        app.dependency_overrides[verify_token] = self.override_verify_token
        mock_delete_account.return_value = {"name": "Account Name", "message": "Delete account with success"}
        response = client.delete("/account?id_user=298&id_account=1")
        assert response.status_code == HTTPStatus.OK
        assert response.json() == {"name": "Account Name", "message": "Delete account with success"}
        

    