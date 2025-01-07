from fastapi import status

from api.v1 import v1_router, admin_router
from exceptions.admin import InvalidTokenError, LoginAlreadyExistsError, IncorrectUsernameOrPasswordError
from schemas.admin import AdminCreateSchema
from utils.validate import create_admin_access_token

from .conftest import client, db_session, load_admin, assert_error


base_endpoint = v1_router.prefix + admin_router.prefix


def test_login_success(client, db_session, load_admin):
    response = client.post(
        f'{base_endpoint}/login',
        data={'username': load_admin.login, 'password': '123'},
    )
    assert response.status_code == status.HTTP_200_OK
    assert 'access_token' in response.json()


def test_login_incorrect_credentials(client, db_session, load_admin):
    response = client.post(
        f'{base_endpoint}/login',
        data={'username': load_admin.login, 'password': 'wrongpass'},
    )
    assert_error(response, IncorrectUsernameOrPasswordError())


def test_create_admin_success(client, db_session, admin):
    token = create_admin_access_token(admin)
    headers = {'Authorization': f'Bearer {token}'}
    data = AdminCreateSchema(login='newadmin', password='newpassword')
    response = client.put(f'{base_endpoint}/create_admin', json=data.model_dump(), headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['login'] == 'newadmin'


def test_create_admin_duplicate(client, db_session, admin):
    token = create_admin_access_token(admin)
    headers = {'Authorization': f'Bearer {token}'}
    data = AdminCreateSchema(login='existingadmin', password='newpassword')
    client.put(f'{base_endpoint}/create_admin', json=data.model_dump(), headers=headers)
    response = client.put(f'{base_endpoint}/create_admin', json=data.model_dump(), headers=headers)
    assert_error(response, LoginAlreadyExistsError())


def test_create_admin_invalid_token(client):
    headers = {'Authorization': 'Bearer invalidtoken'}
    data = AdminCreateSchema(login='newadmin', password='newpassword')
    response = client.put(f'{base_endpoint}/create_admin', json=data.model_dump(), headers=headers)
    assert_error(response, InvalidTokenError())
