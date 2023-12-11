import json
import os
from datetime import datetime as dt
from dataclasses import dataclass
from .connectors.database.json import JsonFileDatabaseConnector
from .config import JSON_DATABASE_NAME


@dataclass(frozen=True)
class ConvertedPricePLN:
    price_in_source_currency: float
    currency: str
    currency_rate: float
    currency_rate_fetch_date: str
    price_in_pln: float


class PriceCurrencyConverterToPLN:

    def convert_to_pln(self, *, currency: str, price: float, rate: float) -> ConvertedPricePLN:
        """
        Method convert given price, rate and currecny to ConvertedPricePLN object
        :param currency: str currency code, i.e "EUR"
        :param price: float, sys.argv
        :return: ConvertedPricePLN object
        """
        price_in_source_currency = price / rate
        currency_rate_fetch_date = dt.now().strftime('%Y-%m-%d')

        return ConvertedPricePLN(price_in_source_currency=price_in_source_currency, currency=currency,
                                 currency_rate=rate, currency_rate_fetch_date=currency_rate_fetch_date,
                                 price_in_pln=price)
