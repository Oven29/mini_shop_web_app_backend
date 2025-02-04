from typing import List

from exceptions.user import WrongAuthData
from schemas.user import UserAuthSchema, UserSchema
from schemas.order import OrderSchema
from utils.validate import validate_init_data
from .base import AbstractService


class UserService(AbstractService):
    async def auth(self, auth_data: UserAuthSchema) -> UserSchema:
        if not validate_init_data(auth_data.init_data):
            raise WrongAuthData

        async with self.uow:
            user = auth_data.init_data_unsafe.user

            db_user, created = await self.uow.user.get_or_crete(
                user_id=user.id,
                defaults={
                    'username': user.username,
                    'first_name': user.first_name,
                },
            )

            if not created and (db_user.username != user.username or db_user.first_name != user.first_name):
                await self.uow.user.update(
                    id=db_user.id,
                    username=user.username,
                    first_name=user.first_name,
                )
                await self.uow.commit()

            if created:
                await self.uow.commit()

            return await db_user.to_schema()

    async def get_all(self) -> List[UserSchema]:
        async with self.uow:
            res = await self.uow.user.select()
            return [await e.to_schema() for e in res]

    async def get_orders(self, user: UserSchema) -> List[OrderSchema]:
        async with self.uow:
            res = await self.uow.order.select(user_id=user.user_id)
            return [await e.to_schema() for e in res]
