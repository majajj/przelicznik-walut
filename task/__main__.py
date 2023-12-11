import sys
from logging import getLogger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import DatabaseError
from .connectors.prod import conf_db as conf
from .connectors.prod import model

from .connectors.database.json import JsonFileDatabaseConnector
from .connectors.database.database import SqliteDatabaseConnector
from .connectors.local.file_reader import JsonFileReader
from .connectors.local.api_reader import ApiReader

logger = getLogger(__name__)

try:
    source, currency, price = sys.argv[2], sys.argv[3], float(sys.argv[4])

    if source == 'plik':
        reader = JsonFileReader()
        data = reader.process_data(currency, price)
    elif source == 'nbp':
        reader = ApiReader()
        data = reader.process_data(currency, price)
    else:
        raise Exception("Source is not corrected, please select either 'plik' or 'nbp' ")

    if sys.argv[1] == 'dev':
        conn = JsonFileDatabaseConnector()
        conn.save(data)

    elif sys.argv[1] == 'prod':
        engine = create_engine('sqlite:///db_test')
        session = scoped_session(sessionmaker(engine))
        model.Base.metadata.bind = engine
        model.Base.metadata.create_all(engine)
        model = conf.Database(session)

        sql = SqliteDatabaseConnector()
        sql.save(data, session)
        sql.get_all(session)



    logger.info("Job done!")
except DatabaseError as de:
    print(de)
except ConnectionError as ce:
    print(ce)
except ValueError as ve:
    print(ve)
except Exception as err:
    print(err)

