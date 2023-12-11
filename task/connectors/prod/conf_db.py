from .model import CurrencyRate

class Database:
    def __init__(self, session):
        self.session = session

    def get_currency_rates(self):
        return self.session.query(CurrencyRate).all()