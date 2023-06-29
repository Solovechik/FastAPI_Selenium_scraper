import datetime

from pydantic import BaseModel


class CreateGoodIn(BaseModel):
    link: str


class CreateGoodOut(BaseModel):
    id: int
    title: str
    description: str
    rating: float
    link: str

    class Config:
        orm_mode = True


class CreateGoodErrorOut(BaseModel):
    error: str


class GoodIdIn(BaseModel):
    id: int


class DeleteGoodOut(BaseModel):
    deletion: bool
    details: str


class GetPricesOut(BaseModel):
    good_id: int
    price: float
    added_at: datetime.datetime

    class Config:
        orm_mode = True
