from .base import SQLAlchemyRepository
from ..models.admin import Admin


class AdminRepository(SQLAlchemyRepository[Admin]):
    model = Admin
