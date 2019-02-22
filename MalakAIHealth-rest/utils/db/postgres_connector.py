import pandas as pd
import logging
from sqlalchemy import create_engine, MetaData

from utils.config import ConfigMalakAI
from .sql_connector import SQLConnector

"""
Postgres connection engine.
"""
logger = logging.getLogger('PostgresConnector')

class PostgresConnector(SQLConnector):
    _engine = None
    _metadata = None
    _session = None

    @staticmethod
    def get_hostname():
        return ConfigMalakAI().get('Postgres', 'host_name', 'localhost')

    @staticmethod
    def get_port():
        return ConfigMalakAI().get('Postgres', 'port', '3306')

    @staticmethod
    def get_username():
        return ConfigMalakAI().get('Postgres', 'user_name', 'myuser')

    @staticmethod
    def get_password():
        return ConfigMalakAI().get('Postgres', 'password', '')

    @staticmethod
    def get_db():
        return ConfigMalakAI().get('Postgres', 'database', 'zbsc')

    @staticmethod
    def get_bulk_insert():
        return int(ConfigMalakAI().get('Postgres', 'bulk_insert', '200'))

    @staticmethod
    def get_bulk_select():
        return int(ConfigMalakAI().get('Postgres', 'bulk_select', '1000'))

    @staticmethod
    def get_dialect():
        return 'postgresql'

    @staticmethod
    def get_str_type(length):
        return "VARCHAR("+str(length)+")"

    @staticmethod
    def get_engine():
        # TODO make it configurable
        # This encoding creates an issue with handling blob, I believe the client tries to encode the blob in latin-1
        # which of course does not work. Solution???
        # by default this is the value in the postgresql.conf file, which often defaults to SQL_ASCII.
        # Typically, this can be changed to utf-8 or latin-1
        if PostgresConnector._engine is None:
            url = 'postgresql://' + \
                PostgresConnector.get_username() + ':' + \
                '*@' + \
                PostgresConnector.get_hostname() + ':' + \
                PostgresConnector.get_port() + '/' + \
                PostgresConnector.get_db()
            logger.info('Database connection: '+url)
            Log.info('Database connection: '+url)

            PostgresConnector._engine = create_engine(
                'postgresql://' +
                PostgresConnector.get_username() + ':' +
                PostgresConnector.get_password() + '@' +
                PostgresConnector.get_hostname() + ':' +
                PostgresConnector.get_port() + '/' +
                PostgresConnector.get_db(),
                pool_size=30,
                max_overflow=-1
            )
        return PostgresConnector._engine
