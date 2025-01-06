from fastapi import status

from .base import BaseApiError


class MediaNotFoundError(BaseApiError):
    class Model(BaseApiError.Model):
        status_code: int = status.HTTP_404_NOT_FOUND
        msg: str = 'File with media_id={media_id} not found'
        media_id: str = ''

    def __init__(self, media_id: str) -> None:
        super().__init__(media_id=media_id)


class FileTooLargeError(BaseApiError):
    class Model(BaseApiError.Model):
        status_code: int = status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
        msg: str = 'File too large'


class NotAvaliableExtensionError(BaseApiError):
    class Model(BaseApiError.Model):
        status_code: int = status.HTTP_400_BAD_REQUEST
        msg: str = 'Not avaliable extension'
