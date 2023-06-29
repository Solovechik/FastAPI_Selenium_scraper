from sqlalchemy import Row
from sqlalchemy.orm import Session

from models import Good


def db_get_good_links(db: Session) -> list[Row]:
    goods: list[Row] = db.query(Good.id, Good.link).all()

    return goods


def db_update_price(db: Session, good_id: int, price: float) -> None:
    db.query(Good).filter_by(id=good_id).update({'price': price})
    db.commit()
