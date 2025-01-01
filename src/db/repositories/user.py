from .base import SQLAlchemyRepository
from ..models.user import User


class UserRepository(SQLAlchemyRepository[User]):
    pass
