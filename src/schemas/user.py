from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class WebAppUser(BaseModel):
    """https://core.telegram.org/bots/webapps#webappuser"""
    id: int  # unique identifier for the user or bot
    is_bot: Optional[bool] = None  # True if this user is a bot, returns in receiver field only
    first_name: str  # First name of the user or bot
    last_name: Optional[str] = None  # Last name of the user or bot
    username: Optional[str] = None  # Username of the user or bot
    language_code: Optional[str] = None  # IETF language tag of the user's language
    is_premium: Optional[bool] = None  # True, if this user is a Telegram Premium user
    added_to_attachment_menu: Optional[bool] = None  # True, if this user added the bot to the attachment menu
    allows_write_to_pm: Optional[bool] = None  # True, if this user allowed the bot to message them
    photo_url: Optional[str] = None  # URL of the user’s profile photo


class WebAppChat(BaseModel):
    """https://core.telegram.org/bots/webapps#webappchat"""
    id: int  # unique identifier for this chat
    type: str  # Type of chat: "group", "supergroup", or "channel"
    title: str  # Title of the chat
    username: Optional[str] = None  # Username of the chat (optional)
    photo_url: Optional[str] = None  # URL of the chat's photo (optional)


class WebAppInitData(BaseModel):
    """https://core.telegram.org/bots/webapps#webappinitdata"""
    query_id: Optional[str] = None  # Unique identifier for the Mini App session
    user: Optional[WebAppUser] = None  # Data about the current user
    receiver: Optional[WebAppUser] = None  # Data about the chat partner (only for private chats)
    chat: Optional[WebAppChat] = None  # Data about the chat (for group chats, supergroups, channels)
    chat_type: Optional[str] = None  # Type of the chat ("sender", "private", "group", etc.)
    chat_instance: Optional[str] = None  # Global identifier for the chat
    start_param: Optional[str] = None  # The value of the startattach parameter passed via link
    can_send_after: Optional[int] = None  # Time in seconds after which a message can be sent
    auth_date: Optional[int] = None  # Unix time when the form was opened
    hash: str  # A hash of all passed parameters
    signature: Optional[str] = None  # A signature of all passed parameters (excluding hash)


class UserAuthSchema(BaseModel):
    init_data: str
    init_data_unsafe: WebAppInitData


class UserSchema(BaseModel):
    user_id: int
    username: Optional[str] = None
    first_name: str
    register_date: Optional[datetime] = None
