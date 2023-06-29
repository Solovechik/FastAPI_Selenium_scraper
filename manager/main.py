from typing import Type, Union

from fastapi import FastAPI, Depends, Response
from sqlalchemy.orm import Session

from . import models
from .models import Good
from .crud import db_get_or_create_good, db_delete_good, db_get_good_list, db_get_good_prices
from .db import engine, SessionLocal
from .schemas import CreateGoodIn, CreateGoodOut, GoodIdIn, DeleteGoodOut, GetPricesOut, CreateGoodErrorOut
from .utils import shop_getter_factory

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


def get_db() -> Session:
    with SessionLocal() as session:
        yield session


@app.post('/good/add/', response_model=Union[CreateGoodOut, CreateGoodErrorOut])
def add_good(response: Response, item: CreateGoodIn, db: Session = Depends(get_db)):
    good_response: dict = shop_getter_factory(item.link)

    if good_response['error_code']:
        response.status_code = good_response['status_code']
        return {'error': good_response['result']}

    good: Good = db_get_or_create_good(db, {**good_response['result'], 'link': item.link})

    return {
        'id': good.id,
        'title': good.title,
        'description': good.description,
        'rating': good.rating,
        'link': good.link
    }


@app.delete('/good/delete/', response_model=DeleteGoodOut)
def delete_good(response: Response, good_id: GoodIdIn, db: Session = Depends(get_db)):
    deletion: int = db_delete_good(db, good_id.id)

    if not deletion:
        response.status_code = 404
        return {
            'deletion': False,
            'details': f'The good with id {good_id.id} does not exist.'
        }

    return {
        'deletion': True,
        'details': f'The good with id {good_id.id} has been deleted.'
    }


@app.get('/good/list/', response_model=list[CreateGoodOut])
def list_goods(db: Session = Depends(get_db)):
    goods: list[Type[Good]] = db_get_good_list(db)

    return goods


@app.get('/good/prices/', response_model=list[GetPricesOut])
def list_good_prices(good_id: GoodIdIn, db: Session = Depends(get_db)):
    good_prices: list[Type[Good]] = db_get_good_prices(db, good_id.id)

    return good_prices
