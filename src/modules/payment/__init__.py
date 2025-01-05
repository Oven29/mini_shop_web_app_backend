from typing import Dict, Tuple

from core.config import settings
from .base import BasePayment
from .crypto_bot import CryptoBotPayment
from .yookassa import YookassaPayment

methods: Tuple[BasePayment, ...] = (
    CryptoBotPayment(settings.cryptobot),
    YookassaPayment(settings.yookassa),
)
name_to_method: Dict[str, BasePayment] = {m.name: m for m in methods}
