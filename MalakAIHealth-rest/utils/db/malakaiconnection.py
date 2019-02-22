import logging

logger = logging.getLogger('PostgresConnector')

class MalakAIConnection():
    """
    The MalakAI connection object stores the current connection, transaction and engine details.
    """

    def __init__(self, sql_connector):
        self.sql_connector = sql_connector
        self.connection = sql_connector.get_engine().connect()
        self.transaction = self.connection.begin()

    def commit_and_create_transaction(self):
        self.commit()
        self.new_transaction()

    def rollback_and_create_transaction(self):
        self.rollback()
        self.new_transaction()

    def commit_and_close(self):
        self.commit()
        self.close()

    def new_transaction(self):
        self.transaction = self.connection.begin()

    def commit(self):
        self.transaction.commit()

    def rollback(self):
        self.transaction.rollback()

    def close(self):
        self.connection.close()