from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, String,  Date
from sqlalchemy import Table, Column, Integer, String, Numeric
from sqlalchemy import Sequence

Base = declarative_base()


class CurrencyRate(Base):
    __tablename__ = 'currency_rate'
    __bind_key__ = 'currency_rate'

    id = Column(Integer, primary_key=True, autoincrement=True)
    currency = Column(String(3), nullable=False)
    rate = Column(Numeric(7, 4), nullable=False)
    price_in_pln = Column(Numeric(5, 1), nullable=False)
    date = Column(Date, nullable=False)

    def __repr__(self) -> str:
        return (f"CurrencyRate(id={self.id!r}, name={self.currency!r}, rate={self.rate}, "
                f"price_in_pln={self.price_in_pln}, date={self.date})")
