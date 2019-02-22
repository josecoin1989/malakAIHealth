from .postgres_connector import PostgresConnector

"""
Get the default database connection object based on the configuration file.
"""


class DefaultConnector:

    def get_default(self):
        return PostgresConnector()
