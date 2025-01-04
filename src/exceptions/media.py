from fastapi import status

from .base import BaseException


class MediaNotFoundError(BaseException):
    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self, media_id: str | int) -> None:
        self.message = f'File with {media_id=} not found'
        super().__init__(self.message)


class FileTooLargeError(BaseException):
    status_code = status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
    message = 'File too large'


class NotAvaliableExtensionError(BaseException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = 'Not avaliable extension'
