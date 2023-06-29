from typing import Type

from sqlalchemy.orm import Session

from .models import Good, PriceHistory


def db_get_or_create_good(db: Session, good: dict) -> Good:
    instance: Good | None = db.query(Good).filter_by(**good).first()

    if instance:
        return instance

    new_good: Good = Good(**good)
    db.add(new_good)
    db.commit()

    return new_good


def db_delete_good(db: Session, good_id: int) -> int:
    deletion: int = db.query(Good).filter_by(id=good_id).delete()
    db.commit()

    return deletion


def db_get_good_list(db: Session) -> list[Type[Good]]:
    goods: list[Type[Good]] = db.query(Good).order_by(Good.id).all()

    return goods


def db_get_good_prices(db: Session, good_id: int) -> list[Type[PriceHistory]]:
    prices: list[Type[PriceHistory]] = (
        db.query(PriceHistory)
        .filter_by(good_id=good_id)
        .order_by(PriceHistory.added_at.desc())
        .all()
    )

    return prices
