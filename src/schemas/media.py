from typing import Optional
from pydantic import BaseModel

from enums.media import TypeMedia


class MediaSchema(BaseModel):
    id: int
    media_id: Optional[str] = None
    type: Optional[TypeMedia] = None
