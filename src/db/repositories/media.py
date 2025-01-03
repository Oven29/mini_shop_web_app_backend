from .base import SQLAlchemyRepository
from ..models.media import Media


class MediaRepository(SQLAlchemyRepository[Media]):
    model = Media
