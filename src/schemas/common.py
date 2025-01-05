from pydantic import BaseModel


class HttpOk(BaseModel):
    status: str = 'ok'
