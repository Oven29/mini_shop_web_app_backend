from datetime import datetime
from typing import Optional
from sqlalchemy import DateTime, Enum, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from enums.media import TypeMedia, LocationMedia
from schemas.media import MediaSchema
from utils.other import get_rand_string
from ..base import Base


class Media(Base):
    __tablename__ = 'media'
    __schema__ = MediaSchema

    media_id: Mapped[str] = mapped_column(String(64), default=lambda: get_rand_string(64), unique=True)
    weight: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    type: Mapped[TypeMedia] = mapped_column(Enum(TypeMedia, native_enum=False))
    location: Mapped[LocationMedia] = mapped_column(Enum(LocationMedia, native_enum=False))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    filename: Mapped[str] = mapped_column(Text)
