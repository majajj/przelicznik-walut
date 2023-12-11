import pytest
from dataclasses import FrozenInstanceError
from .currency_converter import PriceCurrencyConverterToPLN, ConvertedPricePLN
from task.connectors.database.test_database import converted_price_pln

def test_converted_price_pln_freeze(converted_price_pln):
    cpp = converted_price_pln
    with pytest.raises(FrozenInstanceError):
        cpp.price_in_source_currency=50

def test_convert_to_pln():
    pcc = PriceCurrencyConverterToPLN()
    result = pcc.convert_to_pln(currency="EUR", price=25.0, rate=5)
    assert isinstance(result, ConvertedPricePLN)

def test_convert_to_pln_price_type():
    pcc = PriceCurrencyConverterToPLN()
    with pytest.raises(TypeError):
        result = pcc.convert_to_pln(currency="EUR", price='25.0', rate=5)

def test_convert_to_pln_rate_type():
    pcc = PriceCurrencyConverterToPLN()
    with pytest.raises(TypeError):
        result = pcc.convert_to_pln(currency="EUR", price=25.0, rate='5')