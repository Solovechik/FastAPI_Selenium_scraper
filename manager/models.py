from datetime import datetime

from sqlalchemy import String, Text, Float, Numeric, Integer, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .db import Base


class Good(Base):
    __tablename__ = 'goods_to_monitor'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=True)
    rating: Mapped[float] = mapped_column(Float, nullable=True)
    link: Mapped[str] = mapped_column(String(500), nullable=False)
    prices: Mapped[list['PriceHistory']] = relationship(back_populates='good')


class PriceHistory(Base):
    __tablename__ = 'price_history'
    id: Mapped[int] = mapped_column(primary_key=True)
    good_id: Mapped[int] = mapped_column(Integer, ForeignKey('goods_to_monitor.id'))
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    added_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    good: Mapped['Good'] = relationship(back_populates='prices')
