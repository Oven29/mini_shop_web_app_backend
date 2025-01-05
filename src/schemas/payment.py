from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

from enums.order import InvoiceStatus


class InvoiceSchema(BaseModel):
    id: Optional[int] = None
    pay_id: str
    amount: float
    status: InvoiceStatus
    method: str
    url: Optional[str] = None
    created_at: datetime


class InvoiceCreateSchema(BaseModel):
    method: str
    amount: float = Field(..., ge=100, le=1000000, description="Amount must be between 100 and 1,000,000")
    description: Optional[str] = None
