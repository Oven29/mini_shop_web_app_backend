from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from enums.order import InvoiceStatus


class InvoiceSchema(BaseModel):
    id: Optional[int] = None
    pay_id: str
    amount: float
    status: InvoiceStatus
    method: str
    url: Optional[str] = None
    created_at: Optional[datetime] = None


class InvoiceCreateSchema(BaseModel):
    amount: float
    description: Optional[str] = None
