from typing import Optional
from pydantic import BaseModel

from enums.media import TypeMedia


class MediaSchema(BaseModel):
    media_id: str
    type: Optional[TypeMedia] = None
