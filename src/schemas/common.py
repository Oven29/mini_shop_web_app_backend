from typing import Self
from pydantic import BaseModel, model_validator


class HttpOk(BaseModel):
    status: str = 'ok'


class ErrorResponse(BaseModel):
    status_code: int = 400
    msg: str = ''

    @model_validator(mode='after')
    def validate(self) -> Self:
        if '{' in self.msg:
            self.msg = self.msg.format(**self.model_dump(exclude_unset=True))

        return self


class TokenSchema(BaseModel):
    access_token: str
    token_type: str
