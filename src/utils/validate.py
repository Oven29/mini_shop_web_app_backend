import hmac
import hashlib
from datetime import datetime, timedelta
from typing import Any, Dict
from passlib.context import CryptContext
import jwt

from core.config import settings
from schemas.admin import AdminSchema
from schemas.user import WebAppInitData


def validate_user_init_data(
    init_data: WebAppInitData,
) -> bool:
    data_check_string = f'auth_date={init_data.auth_date}\nquery_id={init_data.query_id}\nuser={init_data.user_validate_string}'
    secret_key = hmac.new(
        key='WebAppData'.encode('utf-8'),
        msg=settings.tg.bot_token.get_secret_value().encode('utf-8'),
        digestmod=hashlib.sha256,
    ).digest()
    hash = hmac.new(
        key=secret_key,
        msg=data_check_string.encode('utf-8'),
        digestmod=hashlib.sha256,
    ).hexdigest()
    return hash == init_data.hash


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def create_jwt_access_token(data: Dict[str, Any]) -> str:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=settings.auth.access_token_expire_minutes)
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, settings.app.secret_key.get_secret_value(), settings.auth.algorithm)


def create_admin_access_token(admin: AdminSchema) -> str:
    return create_jwt_access_token({'sub': f'{admin.id}_{admin.login}'})


def decode_jwt_access_token(token: str) -> Dict[str, Any]:
    return jwt.decode(token, settings.app.secret_key.get_secret_value(), [settings.auth.algorithm])    


def decode_admin_access_token(token: str) -> AdminSchema:
    payload = decode_jwt_access_token(token)
    id, login = payload['sub'].split('_', 1)
    return AdminSchema(id=int(id), login=login)
