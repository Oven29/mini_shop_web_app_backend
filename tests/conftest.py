import json
import os
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker

from api.v1.dependencies import admin_auth, user_auth
from db.models import Base
from db.models.admin import Admin
from db.unitofwork import UnitOfWork, TestUnitOfWork
from main import app
from schemas.admin import AdminSchema
from schemas.user import UserSchema
from utils.validate import hash_password


engine = create_engine(f'sqlite:///./test.sqlite', connect_args={'check_same_thread': False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope='session')
def db_session():
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as session:
        yield session
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope='session')
def client():
    app.dependency_overrides[UnitOfWork] = lambda: TestUnitOfWork()
    with TestClient(app) as client:
        yield client


@pytest.fixture
def admin(client):
    admin_schema = AdminSchema(id=1, login='admin')
    app.dependency_overrides[admin_auth] = lambda: admin_schema
    yield admin_schema
    app.dependency_overrides.pop(admin_auth)


@pytest.fixture
def user1(client):
    user_schema = UserSchema(user_id=1, username='username', first_name='Иван')
    app.dependency_overrides[user_auth] = lambda: user_schema
    yield user_schema
    app.dependency_overrides.pop(user_auth)


@pytest.fixture(scope='session')
def load_admin(db_session):
    password = '123'
    admin = Admin(login='admin', hashed_password=hash_password(password))
    db_session.add(admin)
    db_session.commit()
    yield admin
