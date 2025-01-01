from typing import Optional
from pydantic import BaseModel


class WebAppUser(BaseModel):
    id: int
    is_bot: Optional[bool] = None
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    language_code: Optional[str] = None
    is_premium: Optional[bool] = False
    added_to_attachment_menu: Optional[bool] = False
    allows_write_to_pm: Optional[bool] = True
    photo_url: Optional[str] = None


class WebAppInitData(BaseModel):
    query_id: Optional[str] = None
    user: Optional[WebAppUser] = None
    start_param: Optional[str] = None
    user_validate_string: str
    auth_date: int
    hash: str
