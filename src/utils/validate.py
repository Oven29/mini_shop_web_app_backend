import hmac
import hashlib
from datetime import datetime, timedelta
import time
from typing import Any, Dict
from passlib.context import CryptContext
import jwt
import urllib

from core.config import settings
from schemas.admin import AdminSchema
from schemas.user import UserSchema


def validate_init_data(init_data: str, timelife: int = 6000) -> bool:
    vals = dict(urllib.parse.parse_qsl(init_data))
    data_check_string = '\n'.join(f'{k}={v}' for k, v in sorted(vals.items()) if k != 'hash')

    secret_key = hmac.new('WebAppData'.encode(), settings.tg.bot_token.get_secret_value().encode(), hashlib.sha256).digest()
    hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    auth_date = int(vals['auth_date'])

    return hash == vals['hash'] and auth_date < time.time() < auth_date + timelife


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


def create_user_access_token(user: UserSchema) -> str:
    return create_jwt_access_token({'sub': f'{user.user_id}_{user.username}_{user.first_name}'})


def decode_jwt_access_token(token: str) -> Dict[str, Any]:
    return jwt.decode(token, settings.app.secret_key.get_secret_value(), [settings.auth.algorithm])    


def decode_admin_access_token(token: str) -> AdminSchema:
    payload = decode_jwt_access_token(token)
    id, login = payload['sub'].split('_', 1)
    return AdminSchema(id=int(id), login=login)


def decode_user_access_token(token: str) -> UserSchema:
    payload = decode_jwt_access_token(token)
    user_id, username, first_name = payload['sub'].split('_', 2)
    return UserSchema(user_id=int(user_id), username=username, first_name=first_name)
