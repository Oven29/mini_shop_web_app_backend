from fastapi import APIRouter

from .dependencies import AdminAuthDep, UOWDep, UserAuthDep


router = APIRouter(
    prefix='/media',
    tags=['media'],
)


@router.post('/get_upload_url')
async def get_upload_url(
    uow: UOWDep,
    _: AdminAuthDep,
):
    pass


@router.post('/upload/{media_id}')
async def upload(
    media_id: str,
    _: AdminAuthDep,
):
    pass


@router.delete('/delete/{media_id}')
async def delete(
    media_id: str,
    _: AdminAuthDep,
):
    pass


@router.post('/get_destanation_url')
async def get_destanation_url(
    uow: UOWDep,
    _: UserAuthDep,
):
    pass


@router.get('/file/{media_id}')
async def file(
    media_id: str,
):
    pass
