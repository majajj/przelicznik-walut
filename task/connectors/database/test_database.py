import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from task.connectors.prod.model import CurrencyRate
from task.connectors.prod import model
from task.connectors.database.database import SqliteDatabaseConnector
from task.connectors.database.json import JsonFileDatabaseConnector
from task.currency_converter import ConvertedPricePLN

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


@pytest.fixture(scope='session')
def db_engine(request):
    """yields a SQLAlchemy engine which is suppressed after the test session"""
    # db_url = request.config.getoption("--dburl")
    engine_ = create_engine('sqlite:///db_for_test', echo=True)

    yield engine_

    engine_.dispose()


@pytest.fixture(scope='session')
def db_session_factory(db_engine):
    """returns a SQLAlchemy scoped session factory"""
    return scoped_session(sessionmaker(bind=db_engine))


@pytest.fixture(scope='function')
def db_session(db_session_factory):
    """yields a SQLAlchemy connection which is rollbacked after the test"""
    session_ = db_session_factory()

    yield session_

    session_.rollback()
    session_.close()


@pytest.fixture(scope="module")
def currency_rate_single():
    currency_rate = CurrencyRate(
        currency='HUF',
        rate=0.0115,
        price_in_pln=223.0,
        date=datetime.strptime('2023-12-11', '%Y-%m-%d')
    )
    return currency_rate


@pytest.fixture(scope="module")
def converted_price_pln():
    converted_price_pln = ConvertedPricePLN(price_in_source_currency=50.290, currency='EUR',
                                            currency_rate=4.3746, currency_rate_fetch_date='2023-12-11',
                                            price_in_pln=220.0)
    return converted_price_pln


def test_currency_rate_insert(db_session, currency_rate_single):
    db_session.add(currency_rate_single)
    db_session.commit()
    currency = db_session.query(CurrencyRate).filter_by(currency="HUF").first()
    assert currency.currency == 'HUF'

def test_select_type(db_session, currency_rate_single):
    conn = SqliteDatabaseConnector()
    result = conn.get_all(db_session)
    assert type(result) is list

def test_select_type2(db_session, currency_rate_single):
    conn = SqliteDatabaseConnector()
    result = conn.get_all(db_session)
    assert isinstance(result[0], CurrencyRate)


def test_save(db_session, converted_price_pln):
    conn = SqliteDatabaseConnector()
    result = conn.save(entity=converted_price_pln, session=db_session)
    assert type(result) is int


def test_converted_price_pln(db_session, converted_price_pln):
    with pytest.raises(TypeError):
        ConvertedPricePLN(price_in_source_currency=50.290, currency='EUR',
                                         currency_rate_fetch_date='2023-12-11',
                                         price_in_pln=220.0)


def test_json_file_get_all():
    jfdc = JsonFileDatabaseConnector()
    result = jfdc.get_all()
    assert type(result) is list


def test_json_file_get_all():
    jfdc = JsonFileDatabaseConnector()
    result = jfdc.get_all()
    assert result[0].get("currency") == "eur"

def test_file_save(converted_price_pln):
    jfdc = JsonFileDatabaseConnector()
    result = jfdc.save(converted_price_pln)
    assert type(result) is int
