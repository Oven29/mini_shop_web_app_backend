from typing import Optional
from pydantic import BaseModel

from enums.media import TypeMedia


class MediaSchema(BaseModel):
    id: Optional[int] = None
    media_id: Optional[str] = None
    type: Optional[TypeMedia] = None
    url: Optional[str] = None
