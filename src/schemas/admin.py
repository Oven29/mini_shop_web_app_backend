from pydantic import BaseModel


class AdminSchema(BaseModel):
    id: int
    login: str


class Token(BaseModel):
    access_token: str
    token_type: str


class AdminCreateSchema(BaseModel):
    login: str
    password: str
