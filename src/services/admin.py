from exceptions.admin import IncorrectUsernameOrPasswordError, LoginAlreadyExistsError
from schemas.admin import AdminSchema, AdminCreateSchema
from utils.validate import verify_password, hash_password
from .base import AbstractService


class AdminService(AbstractService):
    async def login(self, login: str, password: str) -> AdminSchema:
        async with self.uow:
            admin = await self.uow.admin.get(login=login)
            if admin is None:
                raise IncorrectUsernameOrPasswordError

            if not verify_password(password, admin.hashed_password):
                raise IncorrectUsernameOrPasswordError

            return await admin.to_schema()

    async def create(self, admin: AdminCreateSchema) -> AdminSchema:
        async with self.uow:
            res = await self.uow.admin.get(login=admin.login)
            if res is not None:
                raise LoginAlreadyExistsError
            res = await self.uow.admin.create(
                login=admin.login,
                hashed_password=hash_password(admin.password),
            )
            await self.uow.commit()
            return await res.to_schema()
