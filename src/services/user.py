from typing import List

from schemas.user import UserSchema
from schemas.order import OrderSchema
from .base import AbstractService


class UserService(AbstractService):
    async def auth(self, user: UserSchema) -> UserSchema:
        async with self.uow:
            db_user, created = await self.uow.user.get_or_crete(
                user_id=user.user_id,
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

            user.register_date = db_user.register_date
            return user

    async def get_all(self) -> List[UserSchema]:
        async with self.uow:
            res = await self.uow.user.select()
            return [await e.to_schema() for e in res]

    async def get_orders(self, user: UserSchema) -> List[OrderSchema]:
        async with self.uow:
            res = await self.uow.order.select(user_id=user.user_id)
            return [await e.to_schema() for e in res]
