from fastapi import status

from exceptions.admin import InvalidTokenError, LoginAlreadyExistsError, IncorrectUsernameOrPasswordError
from schemas.admin import AdminSchema, AdminCreateSchema
from utils.validate import create_admin_access_token

from .conftest import client, db_session, load_admin


base_endpoint = '/v1/admin'


def test_login_success(client, db_session, load_admin):
    response = client.post(
        f'{base_endpoint}/login',
        data={'username': load_admin.login, 'password': '123'},
    )
    assert response.status_code == 200
    assert 'access_token' in response.json()


def test_login_incorrect_credentials(client, db_session, load_admin):
    response = client.post(
        f'{base_endpoint}/login',
        data={'username': load_admin.login, 'password': 'wrongpass'},
    )
    assert response.status_code == IncorrectUsernameOrPasswordError.status_code
    assert response.json() == IncorrectUsernameOrPasswordError().model.model_dump()


def test_create_admin_success(client, db_session, admin):
    token = create_admin_access_token(admin)
    headers = {'Authorization': f'Bearer {token}'}
    data = AdminCreateSchema(login='newadmin', password='newpassword')
    response = client.put(f'{base_endpoint}/create_admin', json=data.model_dump(), headers=headers)
    assert response.status_code == 200
    assert response.json()['login'] == 'newadmin'


def test_create_admin_duplicate(client, db_session, admin):
    token = create_admin_access_token(admin)
    headers = {'Authorization': f'Bearer {token}'}
    data = AdminCreateSchema(login='existingadmin', password='newpassword')
    client.put(f'{base_endpoint}/create_admin', json=data.model_dump(), headers=headers)
    response = client.put(f'{base_endpoint}/create_admin', json=data.model_dump(), headers=headers)
    assert response.status_code == LoginAlreadyExistsError.status_code
    assert response.json() == LoginAlreadyExistsError().model.model_dump()


def test_create_admin_invalid_token(client):
    headers = {'Authorization': 'Bearer invalidtoken'}
    data = AdminCreateSchema(login='newadmin', password='newpassword')
    response = client.put(f'{base_endpoint}/create_admin', json=data.model_dump(), headers=headers)
    assert response.status_code == InvalidTokenError.status_code
    assert response.json() == InvalidTokenError().model.model_dump()
