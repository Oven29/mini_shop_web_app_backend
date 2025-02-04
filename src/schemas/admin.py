from pydantic import BaseModel


class AdminSchema(BaseModel):
    id: int
    login: str


class AdminCreateSchema(BaseModel):
    login: str
    password: str
