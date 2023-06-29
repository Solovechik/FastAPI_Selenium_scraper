from sqlalchemy import Row
from sqlalchemy.orm import Session

from db import engine
from crud import db_get_good_links, db_update_price
from utils import shop_getter_factory
from apscheduler.schedulers.background import BlockingScheduler

scheduler = BlockingScheduler()


def update_prices() -> None:
    with Session(engine) as session:
        goods: list[Row] = db_get_good_links(session)
        for good_id, link in goods:
            price = shop_getter_factory(link)

            if price['error_code']:
                print(price['result'])
            else:
                db_update_price(session, good_id, price['result'])


scheduler.add_job(update_prices, 'cron', hour='*')
scheduler.start()
