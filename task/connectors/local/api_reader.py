import requests
from task.config import NBP_API_LINK
from task.currency_converter import ConvertedPricePLN, PriceCurrencyConverterToPLN
from task.connectors.database.json import JsonFileDatabaseConnector

class NbpConnector:

    @staticmethod
    def build_url(**kwargs):
        """
        Method build url.
        :param kwargs: currency_exchange: Bool, json: Bool, currency: str
        :return: str url
        """
        url = NBP_API_LINK
        if kwargs.get("currency_exchange"):
            url = url + f'exchangerates/rates/c/{kwargs.get("currency")}'
        if kwargs.get("json"):
            url = url + "?format=json"
        return url

    @staticmethod
    def process_response(response):
        """
        Method process the response, returns either json or ConnectionError
        :param response: request
        :return: json
        """
        if response.status_code == 200:
            return response.json()
        else:
            raise ConnectionError(f'Connection fails due to: {response.status_code} {response.reason}')


    def get_currency_exchange(self, currency):
        """
        Method build url and then send request to API and get response
        :param currency: str currency code, i.e "EUR"
        :return:
        """
        url = self.build_url(currency_exchange=True, json=True, currency=currency)
        r = requests.get(url)
        return self.process_response(r)


class ApiReader(NbpConnector):

    def get_rates(self, currency: str) -> float:
        """
        Method send request to nbp api and get rate
        :param currency: str currency code, i.e "EUR"
        :return: float, rate or ConnectionError
        """
        response = self.get_currency_exchange(currency)
        if response.get('rates'):
            return response.get('rates')[0].get('ask')
        else:
            raise ConnectionError("Currency rate not available. Make sure that currency code is valid.")

    def process_data(self, currency: str, price: float):
        """
        Method to process data, get rate and then convert price and currency
        :param currency:  str currency code, i.e "EUR"
        :param price: float, sys.argv
        :return:
        """
        converter = PriceCurrencyConverterToPLN()
        conn = JsonFileDatabaseConnector()
        rate = self.get_rates(currency)
        return converter.convert_to_pln(currency=currency, price=price, rate=rate)
