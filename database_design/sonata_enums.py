#!/usr/bin/env python
"""
A module containing the abstract base class specification for SQL tables (and views, which act like tables)
"""
from abc import ABC, abstractmethod
from typing import Tuple, List

from psycopg2 import sql

from general_utils.sql_utils import Field, SQLType, SchemaTable, create_table_from_field_sql_type_tuples


class SonataType(object):
    """
    An enum for a sonata type
    """

    @classmethod
    def TYPE_1(cls) -> str:
        return "Type 1"

    @classmethod
    def TYPE_2(cls) -> str:
        return "Type 2"

    @classmethod
    def TYPE_3(cls) -> str:
        return "Type 3"

    @classmethod
    def TYPE_4(cls) -> str:
        return "Type 4"

    @classmethod
    def TYPE_5(cls) -> str:
        return "Type 5"


class PieceType(object):
    """
    An enum for a piece type
    """

    @classmethod
    def SYMPHONY(cls) -> str:
        return "Symphony"

    @classmethod
    def PIANO_SONATA(cls) -> str:
        return "Piano Sonata"

    @classmethod
    def PIANO_CONCERTO(cls) -> str:
        return "Piano Concerto"

    @classmethod
    def VIOLIN_CONCERTO(cls) -> str:
        return "Violin Concerto"

    @classmethod
    def STRING_QUARTER(cls) -> str:
        return "String Quartet"
