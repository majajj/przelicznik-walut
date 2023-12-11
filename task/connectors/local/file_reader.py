# TODO connector for reading local source (example_currency_rates.json) with currency rates
import json
from task.config import FILE_CURRENCY_RATE
from task.currency_converter import PriceCurrencyConverterToPLN
from task.connectors.database.json import JsonFileDatabaseConnector


class JsonFileReader():

    def read_file(self, currency: str) -> float:
        """
        Method to read json file
        :param currency: str currency code, i.e "EUR"
        :return: float, rate or VallueError
        """
        with open(FILE_CURRENCY_RATE, 'r') as f:
            response = json.load(f)
            if response.get(currency.upper()):
                return response[currency.upper()][0]['rate']
            else:
                raise ValueError(f"Currency: {currency} is not available, please try use nbp rates.")


    def process_data(self, currency: str, price: float):
        """
        Method to process data, get rate and then convert price and currency
        :param currency:  str currency code, i.e "EUR"
        :param price: float, sys.argv
        :return:
        """
        converter = PriceCurrencyConverterToPLN()
        conn = JsonFileDatabaseConnector()
        rate = self.read_file(currency=currency)
        return converter.convert_to_pln(currency=currency, price=price, rate=rate)
