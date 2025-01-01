from pydantic import BaseModel


class AdminSchema(BaseModel):
    id: int
    login: str
