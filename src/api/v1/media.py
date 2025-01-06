from fastapi import APIRouter, UploadFile
from fastapi.responses import FileResponse

from exceptions.admin import InvalidTokenError
from exceptions.common import UnauthorizedError
from exceptions.media import FileTooLargeError, MediaNotFoundError, NotAvaliableExtensionError
from schemas.media import MediaSchema
from services.media import MediaService
from .dependencies import AdminAuthDep, UOWDep, UserAuthDep


router = APIRouter(
    prefix='/media',
    tags=['media'],
)


@router.post(
    '/upload',
    responses={
        InvalidTokenError.status_code: InvalidTokenError.error_schema,
        FileTooLargeError.status_code: FileTooLargeError.error_schema,
        NotAvaliableExtensionError.status_code: NotAvaliableExtensionError.error_schema,
    },
)
async def upload(
    uow: UOWDep,
    file: UploadFile,
    _: AdminAuthDep,
) -> MediaSchema:
    return await MediaService(uow).upload(file)


@router.delete(
    '/delete/{media_id}',
    responses={
        InvalidTokenError.status_code: InvalidTokenError.error_schema,
        MediaNotFoundError.status_code: MediaNotFoundError.error_schema,
    },
)
async def delete(
    uow: UOWDep,
    media_id: str,
    _: AdminAuthDep,
) -> MediaSchema:
    return await MediaService(uow).delete(media_id)


@router.post(
    '/get_file_url/{media_id}',
    responses={
        MediaNotFoundError.status_code: MediaNotFoundError.error_schema,
        UnauthorizedError.status_code: UnauthorizedError.error_schema,
    },
)
async def get_file_url(
    uow: UOWDep,
    media_id: str,
    _: UserAuthDep,
) -> MediaSchema:
    return await MediaService(uow).get_file_url(media_id)


@router.get(
    '/{media_id}',
    responses={
        MediaNotFoundError.status_code: MediaNotFoundError.error_schema,
    },
)
async def file(
    uow: UOWDep,
    media_id: str,
) -> FileResponse:
    return await MediaService(uow).file(media_id)
