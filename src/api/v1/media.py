from fastapi import APIRouter, UploadFile
from fastapi.responses import FileResponse

from schemas.media import MediaSchema
from services.media import MediaService
from .dependencies import AdminAuthDep, UOWDep, UserAuthDep


router = APIRouter(
    prefix='/media',
    tags=['media'],
)


@router.post('/upload')
async def upload(
    uow: UOWDep,
    file: UploadFile,
    _: AdminAuthDep,
) -> MediaSchema:
    return await MediaService(uow).upload(file)


@router.delete('/delete/{media_id}')
async def delete(
    uow: UOWDep,
    media_id: str,
    _: AdminAuthDep,
) -> MediaSchema:
    return await MediaService(uow).delete(media_id)


@router.post('/get_file_url/{media_id}')
async def get_file_url(
    uow: UOWDep,
    media_id: str,
    _: UserAuthDep,
) -> MediaSchema:
    return await MediaService(uow).get_file_url(media_id)


@router.get('/{media_id}')
async def file(
    uow: UOWDep,
    media_id: str,
) -> FileResponse:
    return await MediaService(uow).file(media_id)
