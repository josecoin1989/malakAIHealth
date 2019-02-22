import logging

from sqlalchemy import MetaData, Table, inspect, DDL

from .malakaiconnection import MalakAIConnection

"""
Utility functions for a given database connection.

This class is abstract and should be override.
"""


class SQLConnector:

    logger = logging.getLogger('SQLConnector')

    def get_engine(self):
        raise NotImplementedError("Get Connection")

    def get_bulk_insert(self):
        raise NotImplementedError("Get Bulk Insert")

    def get_bulk_select(self):
        raise NotImplementedError("Get Bulk Select")

    def get_dialect(self):
        raise NotImplementedError("Get Dialect")

    def get_metadata(self):
        return MetaData(bind=self.get_engine())

    def drop_table(self,table_name):
        self.get_engine().execute(DDL('DROP TABLE '+table_name))

    def table_exists(self,table_name):
        metadata = MetaData(bind=self.get_engine())
        table = Table(table_name, metadata)
        return table.exists()

    def get_table(self,table_name):
        metadata = MetaData(bind=self.get_engine())
        return Table(table_name, metadata,autoload=True)

    def get_column_names(self,table_name):
        inspector = inspect(self.get_engine())
        t = inspector.get_columns(table_name)
        l = [x['name'] for x in t]
        return l

    def get_columns(self,table_name):
        inspector = inspect(self.get_engine())
        return inspector.get_columns(table_name)

    def add_string_columns(self, table_name, col_list):
        existing_columns = self.get_column_names(table_name)
        columns_to_add = list(filter(lambda x: x not in existing_columns, col_list))
        self.logger.debug('Add '+str(columns_to_add)+' to '+table_name)
        for c in columns_to_add:
            self.add_string_column(table_name, c, 500)
        return

    def add_string_column(self,table_name, new_column, length = 150):
        q = "ALTER TABLE " + table_name + " ADD COLUMN"
        ft = self.get_str_type(length)
        q = q + " " + new_column + " " + ft
        self.logger.debug(q)
        self.get_engine().execute(q)


    def create_connection(self):
        return MalakAIConnection(self)