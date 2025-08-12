from pydantic import BaseModel


class SProductResponse(BaseModel):
    id: int
    title: str
    user_id: int


class SPostCreate(BaseModel):
    title: str

