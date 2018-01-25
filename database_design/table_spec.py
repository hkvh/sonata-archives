#!/usr/bin/env python
"""
A module containing the abstract base class specification for SQL tables (and views, which act like tables)
"""
from abc import ABC, abstractmethod
from typing import Tuple, List

from psycopg2 import sql

from general_utils.sql_utils import Field, SQLType, SchemaTable, create_table_from_field_sql_type_tuples


class TableSpecification(ABC):
    """
    An abstract base class for subclasses that will store the specification for a table or view.

    These objects are not meant to be instantiated - simply use their class methods and properties.
    """

    @classmethod
    @abstractmethod
    def schema_table(cls) -> SchemaTable:
        """
        An abstract method that each subclass must implement to specify their schema and table name

        :return: a SchemaTable object containing their schema and table
        """

    @classmethod
    @abstractmethod
    def field_sql_type_list(cls) -> List[Tuple[Field, SQLType]]:
        """
        An abstract method that each subclass must implement that contains a list of fields and the sql types
        which will be wrapped into a create table script so that creating and modifying the table schema is easy

        :return: a Composable with the script that will be used to create the table - dropping it if it already exists
        """

    @classmethod
    def create_table_sql(cls, drop_if_exists=True) -> sql.Composable:
        """
        Returns a create table sql script for this table using the field_sql_type_list. If drop_if_exists is true
        we will replace the table by drop cascading it

        :param drop_if_exists:
        :return: the create table script as a SQL Composable
        """
        create_table_sql = create_table_from_field_sql_type_tuples(cls.schema_table(), cls.field_sql_type_list())

        if drop_if_exists:
            return sql.SQL("DROP TABLE IF EXISTS {st} CASCADE;\n").format(st=cls.schema_table()) + create_table_sql
        else:
            return create_table_sql

    @classmethod
    @abstractmethod
    def create_constraints_sql(cls) -> sql.Composable:
        """
        Returns a sql script that creates the constraints on this table (like PKs and FKs)

        :return: the sql as a Composable
        """