from datetime import datetime
from ..prod.model import CurrencyRate
from sqlalchemy.exc import DatabaseError


class SqliteDatabaseConnector:

    def save(self, entity: object, session) -> int:
        """
        Save data in sqlite database
        :param entity: object ConvertedPricePLN
        :return: int id in CurrentRate table
        """
        try:
            date_obj = datetime.strptime(entity.currency_rate_fetch_date, '%Y-%m-%d')
            currency_rate = CurrencyRate(currency=entity.currency, rate=entity.currency_rate,
                                         price_in_pln=entity.price_in_pln, date=date_obj)
            session.add(currency_rate)
            session.flush()
            session.commit()
            return currency_rate.id
        except DatabaseError as de:
            raise de.code

    def get_all(self, session) -> list[...]:
        """
        Method selects all data from Currency Rate table
        :param session: session
        :return: dataset
        """
        return session.query(CurrencyRate).all()

    def get_by_id(self, id: int, session) -> object:
        """
        select certain row from Currency Rate object
        :param id: int
        :param session: session
        :return: dataset Currency Rate
        """
        return session.query(CurrencyRate).get(id)
