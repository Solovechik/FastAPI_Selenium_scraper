from sqlalchemy import String, Text, Float, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from db import Base


class Good(Base):
    __tablename__ = 'goods_to_monitor'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=True)
    rating: Mapped[float] = mapped_column(Float, nullable=True)
    link: Mapped[str] = mapped_column(String(500), nullable=False)
