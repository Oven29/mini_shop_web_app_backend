from datetime import datetime
from typing import List, Optional
from sqlalchemy import BigInteger, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base


class User(Base):
    user_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    username: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    first_name: Mapped[str] = mapped_column(String(256), nullable=True)
    register_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
