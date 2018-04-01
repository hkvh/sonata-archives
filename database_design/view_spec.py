#!/usr/bin/env python
"""
A module containing the abstract base class specification for SQL tables (and views, which act like tables)
"""
from abc import ABC, abstractmethod

from psycopg2 import sql, extensions

from general_utils.sql_utils import SchemaTable


class ViewSpecification(ABC):
    """
    An abstract base class for subclasses that will store the specification for a view.

    These objects are not meant to be instantiated - simply use their class methods and properties.
    """

    @classmethod
    @abstractmethod
    def schema_table(cls) -> SchemaTable:
        """
        An abstract method that each subclass must implement to specify their schema and view name (table name)

        :return: a SchemaTable object containing their schema and view name (treated as table name)
        """

    @classmethod
    @abstractmethod
    def view_select_sql(cls, cur: extensions.cursor) -> sql.Composable:
        """
        The abstract methods that subclasses implement that contains the select query that represents the view.
        Includes a cursor in case the view is so tethered to the source tables that it requires dynamic querying
        of the information schema to deduce which columns it should use.

        :param cur: a cursor to the database containing tables
        :return: a select query that will be used for view creation in create_view_sql.
        """

    @classmethod
    def create_view_sql(cls, cur: extensions.cursor, drop_if_exists: bool = True) -> sql.Composable:
        """
        Returns a create view sql script for this view leveraging the view_select_sql. (Do not override).
        Includes a cursor in case the view is so tethered to the source tables that it requires dynamic querying
        of the information schema to deduce which columns it should use.

        :param cur: a cursor to the database containing tables
        :param drop_if_exists: whether to drop cascade the view if already exists, defaults to True
        :return: the create table script as a SQL Composable
        """
        create_sql = sql.SQL('')
        if drop_if_exists:
            create_sql = create_sql + sql.SQL("DROP VIEW IF EXISTS {st} CASCADE;\n").format(st=cls.schema_table())

        return create_sql + sql.SQL("CREATE VIEW {st} AS "
                                    "{vs}\n").format(st=cls.schema_table(), vs=cls.view_select_sql(cur))
