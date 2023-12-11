import pytest
import validators
import requests
from .api_reader import ApiReader
from .file_reader import JsonFileReader
from task.currency_converter import ConvertedPricePLN


###### API READER ###############
def test_get_rates():
    currency = 'DKK'
    ar = ApiReader()
    result = ar.get_rates(currency)
    assert type(result) is float


def test_api_get_rates_wrong_currency():
    currency = 'ABC'
    ar = ApiReader()
    with pytest.raises(ConnectionError):
        result = ar.get_rates(currency)

def test_process_data():
    currency = 'DKK'
    price = 25
    ar = ApiReader()
    result = ar.process_data(currency, price)
    assert isinstance(result, ConvertedPricePLN)


def test_process_data2():
    currency = 'DKK'
    price = '25'
    ar = ApiReader()
    with pytest.raises(TypeError):
        ar.process_data(currency, price)


def test_build_url():
    ar = ApiReader()
    currency = 'SEK'
    result = ar.build_url(currency_exchange=True, json=True, currency=currency)
    assert validators.url(result)


def test_build_url():
    ar = ApiReader()
    currency = 'SEK'
    result = ar.build_url(currency_exchange=False, json=False, currency=currency)
    response = requests.get(result)
    assert response.status_code == 404 and response.reason == "Not Found"


def test_get_currency_exchange():
    ar = ApiReader()
    currency = 'SEK'
    result = ar.get_currency_exchange(currency=currency)
    assert type(result) is dict

def test_get_currency_exchange_currency():
    ar = ApiReader()
    currency = 'ABC'
    with pytest.raises(ConnectionError):
        result = ar.get_currency_exchange(currency=currency)


#################### FILE READER #######################

def test_read_file():
    jfr = JsonFileReader()
    currency = 'EUR'
    result = jfr.read_file(currency)
    assert type(result) is float

def test_read_file():
    jfr = JsonFileReader()
    currency = 'DKK'
    with pytest.raises(ValueError):
        result = jfr.read_file(currency)

def test_process_data_jfr():
    currency = 'CZK'
    price = 25
    ar = JsonFileReader()
    result = ar.process_data(currency, price)
    assert isinstance(result, ConvertedPricePLN)

def test_process_data_jfr2():
    currency = 'CZK'
    price = '25'
    ar = JsonFileReader()
    with pytest.raises(TypeError):
        ar.process_data(currency, price)
