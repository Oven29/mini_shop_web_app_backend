import os
import shutil
from fastapi import UploadFile
from fastapi.responses import FileResponse

from core.config import settings
from db.models.media import Media
from enums.media import TypeMedia, LocationMedia
from exceptions.media import MediaNotFoundError, FileTooLargeError, NotAvaliableExtensionError
from schemas.media import MediaSchema
from utils.other import get_file_size, get_rand_string
from .base import AbstractService


class MediaService(AbstractService):
    async def get_url(self, media_id: str, location: LocationMedia) -> str:
        if location == LocationMedia.LOCAL:
            return f'{settings.project.backend_url}/v1/media/{media_id}'
        raise MediaNotFoundError(media_id)

    async def get_media(self, media_id: str) -> Media:
        res = await self.uow.media.get(media_id=media_id)
        if res is None:
            raise MediaNotFoundError(media_id)
        return res

    async def upload(self, file: UploadFile) -> MediaSchema:
        weight = get_file_size(file.file)
        if weight > settings.file.max_size:
            raise FileTooLargeError

        extension = file.filename.split('.')[-1]
        if extension not in settings.AVAILABLE_EXTENSIONS:
            raise NotAvaliableExtensionError

        media_id = get_rand_string(64)
        file_type = TypeMedia.VIDEO if extension == 'mp4' else TypeMedia.IMAGE
        filename = f'{media_id}.{extension}'
        filepath = os.path.join(settings.dir.uploads, filename)

        with open(filepath, 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)

        async with self.uow:
            res = await self.uow.media.create(
                media_id=media_id,
                weight=weight,
                type=file_type,
                location=LocationMedia.LOCAL,
                filename=filename,
            )
            await self.uow.commit()
            url = await self.get_url(media_id=media_id, location=LocationMedia.LOCAL)
            return await res.to_schema(url=url)

    async def delete(self, media_id: str) -> MediaSchema:
        async with self.uow:
            res = await self.get_media(media_id=media_id)
            await self.uow.media.delete(id=res.id)
            await self.uow.commit()
            return await res.to_schema()

    async def get_file_url(self, media_id: str) -> MediaSchema:
        async with self.uow:
            res = await self.get_media(media_id=media_id)
            url = await self.get_url(media_id=media_id, location=LocationMedia.LOCAL)
            return await res.to_schema(url=url)

    async def file(self, media_id: str) -> FileResponse:
        async with self.uow:
            res = await self.get_media(media_id=media_id)
            return FileResponse(
                path=os.path.join(settings.dir.uploads, res.filename),
            )
