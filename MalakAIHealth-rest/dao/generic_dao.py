"""
The generic_dao package includes shared utilities available for any table interfacing classes in the project.

This class has been purely written for postgres sql and includes:
- create and frop functions
- partition handling
- common queries used on any dataset (filter on dataset_id or cycle_id).
"""

import logging
import re
import pandas as pd
from sqlalchemy.sql.ddl import CreateTable, DDL
from sqlalchemy import select, delete


class GenericDAO:
    """
    Abstract class for DAO objects.
    """
    logger = logging.getLogger('GenericDAO')

    def __init__(self, connection, id_column='id', partition_columns=list(), foreign_key_columns=list(), unique_columns=list()):
        """
        Instanciate a new table in the connector metadata.

        The last three arguments are available for handling partition tables.

        :param connection: The connection
        :param id_column: The name of the id column
        :param partition_columns: list of column to partition on. At the moment only one column can be specified.
        :param foreign_key_columns:
            The list of column key. Each element should be a tuple of 2 to 4 element:
                - target table,
                - column name of the target table
                - current table field (optional as in most case it is `target_table`_`column_name`
                - True if the target table is a partition table, false otherwise
        :param unique_columns:
            The list of columns in string format on which to apply a unique constraint
        """
        self.connection = connection
        self.connector = connection.sql_connector
        self._connection = connection.connection
        self._table = None
        self._table_name = None
        self._partition_columns = partition_columns
        self._id_column = id_column
        self._foreign_key_columns = foreign_key_columns
        self._unique_columns = unique_columns

    def create(self):
        """
        Create a new table
        :return:
        """
        if not self.connector.table_exists(self._table_name):
            create_str = self.create_statement()
            self.logger.info(create_str)
            self._connection.execute(DDL(create_str))
        else:
            self.logger.info('Table ' + self._table_name+' already exists')
    def create_statement(self):
        """
        Modify the create statement for handling partitions.
        :return: the string statement to run.
        """
        create_str = str(CreateTable(self._table).compile(self.get_engine()))
        if len(self._partition_columns) > 0:
            if 'postgresql' == str(self.connector.get_dialect()):
                if self._id_column:
                    create_str = re.sub('(\s+)'+self._id_column+' INTEGER,', self._id_column+' SERIAL,', create_str)
                create_str += ' PARTITION BY LIST ("'+','.join(self._partition_columns)+'")'
            else:
                raise Exception('Partitions not supported for the dialect '+str(self.get_engine().get_dialect())+'!')
        return create_str

    def __add_reference_in_table(self, partition_value_dic, table_name, ref_column_name, column_name = None, use_part_ref=False):
        """
        Add extra constraints on a child table (partition table).
        :param partition_value_dic:
        :param table_name:
        :param ref_column_name:
        :param column_name:
        :param use_part_ref:
        :return:
        """
        if column_name is None:
            column_name = table_name+'_' + ref_column_name
        if use_part_ref:
            return column_name+' references '+table_name+'_'+str(partition_value_dic[column_name])+'(' + ref_column_name + ')'
        return column_name+' references '+table_name+'(' + ref_column_name + ')'

    def add_partition(self, partition_value, partition_value_dic):
        """
        Add a partition to a table.

        :param partition_value: The value of the partition. The framework supports one value per partition
        :param partition_value_dic: In case of dynamic reference (foreign key on a partition table), the value is required in a dictionary
        :return:
        """
        if self.connector.table_exists(self._table_name+'_'+str(partition_value)):
            return

        if len(self._partition_columns) > 0:
            add_partition_str = self.add_partition_statement(partition_value, partition_value_dic)
            self.logger.info(add_partition_str)
            self._connection.execute(DDL(add_partition_str))

    def add_partition_statement(self, partition_value, partition_value_dic):
        """
        Returns a string statement to create a partition.
        :param partition_value:
        :param partition_value_dic:
        :return:
        """
        if 'postgresql' != str(self.connector.get_dialect()):
            raise Exception('Partitions not supported for the dialect ' + str(self.get_engine().get_dialect()) + '!')

        q = 'CREATE TABLE '+self._table_name+'_'+str(partition_value)+' PARTITION OF '+self._table_name\

        q += ' FOR VALUES IN ('+str(partition_value)+')'
        return q

    def drop(self):
        """
        Drop a table
        :return:
        """
        self.logger.debug('Drop table ' + self._table_name+'...')
        try:
            self._connection.execute(DDL('DROP TABLE '+self._table_name+ ' CASCADE'))
            self.logger.info('Droped table '+self._table_name)
        except Exception as e:
            self.logger.warning('Fail to drop '+self._table_name)


    def get_engine(self):
        """
        Get the engine from the connector.
        :return:
        """
        return self.connector.get_engine()

    def get_metadata(self):
        """
        Get the metadata.
        :return:
        """
        return self.connector.get_metadata()


    def _insert_in_bulk(self,df):
        """
        Insert the data frame into a table.
        :param df:
        :return:
        """
        df.to_sql(self._table_name, self._connection, if_exists='append', index=False,
                  chunksize=self.connector.get_bulk_insert())

    def get_record_from_id(self, id):
        """
        Get a full record dictionary from an id
        :param id:
        :return:
        """
        id_s = select([self._table]).where(self._table.c.id == id)
        df = pd.read_sql(id_s, self._connection)
        dd = df.to_dict('records')
        if not dd or len(dd) == 0:
            return None
        return dd[0]

    def select_filter_dataset_id(self, dataset_id, use_bulk=False):
        """
        Select all records filter on a dataset id.
        :param dataset_id:
        :param use_bulk:
        :return:
        """
        sel_q = select([self._table]).where(self._table.c.dataset_id == dataset_id)
        if use_bulk:
            return pd.read_sql(sel_q, self._connection, chunksize=self.connector.get_bulk_select())
        else:
            return pd.read_sql(sel_q, self._connection)

    def select_filter_cycle_id(self, cycle_id, use_bulk=False):
        """
        Select all records filter on a cycle id.
        :param cycle_id:
        :param use_bulk:
        :return:
        """
        sel_q = select([self._table]).where(self._table.c.cycle_id == cycle_id)
        if use_bulk:
            return pd.read_sql(sel_q, self._connection, chunksize=self.connector.get_bulk_select())
        else:
            return pd.read_sql(sel_q, self._connection)

    def select_all(self, use_bulk=False):
        sel_q = select([self._table])
        if use_bulk:
            return pd.read_sql(sel_q, self._connection, chunksize=self.connector.get_bulk_select())
        else:
            return pd.read_sql(sel_q, self._connection)

    def _get_df(self, sel_q, use_bulk = False):
        """

        :param sel_q:
        :param use_bulk:
        :return:
        """
        if use_bulk:
            return pd.read_sql(sel_q, self._connection, chunksize=self.connector.get_bulk_select())
        else:
            return pd.read_sql(sel_q, self._connection)

    def delete_all(self, dataset_id):
        """
        Deletes records from the db for a given dataset id.
        :param dataset_id:
        :return:
        """
        statement = delete(self._table).where(self._table.c.dataset_id == dataset_id)
        result = self._connection.execute(statement)
        return result.rowcount
