#!/usr/bin/env python
"""
This module contains the core Composable subclasses that we made to handle SchemaTables and Fields.

SchemaTables will always be unquoted and thus directly extend Composable while Fields will always be quoted
and thus
"""
from typing import Union, List, Tuple, Dict, Any

from psycopg2 import sql, extensions

from general_utils.postgres_utils import LocalhostCursor
from general_utils.type_helpers import validate_is_int


class Field(sql.Identifier):
    """
    A composable instance for a field that allows it to work as an element in a query using psycopg's sql module.

    This is a clone of sql.Identifier except that it allows for an optional display name and it is hashable (as the
    unquoted string value). This usefully allows us to store sets or dicts of Fields as if they were strings.

    Note that by subclassing Identifier directly we inherit its useful ability to properly quote things with escaping.
    """
    def __init__(self, name: str, display_name: Union[str, None] = None):
        """
        Constructs a field with a raw name and an optional display name.

        If no display_name is provided, then we will use the raw_name as the display name.

        :param name: the name of the field (required)
        :param display_name: the display name (optional)
        """
        # This assigned the name to be "_wrapped"
        super().__init__(name)

        self._display_name = display_name if display_name is not None else name

    def __hash__(self):
        """
        Implements hash for the Field by using the hash of its wrapped string
        :return:
        """
        return self.string.__hash__()

    @property
    def name(self) -> str:
        """
        Returns the field name (unquoted)
        :return: the field name
        """
        return self.string

    @property
    def display_name(self) -> str:
        """
        Returns the display name of the field
        :return: the field display name
        """
        return self._display_name

    def clone_with_new_display_name(self, display_name: str) -> 'Field':
        """
        Clones this field and changes its display name (keeps the field name)
        :return: a new field instance with the same name but the new field display name
        """
        return Field(self.name, display_name)


class Schema(sql.Identifier):
    """
    A composable instance for a schema that allows it to work as an element in a query using psycopg's sql module.

    Right now a pure clone of Identifier and stores the constructor in the "_wrapped" property
    """


class Table(sql.Identifier):
    """
    A composable instance for a schema that allows it to work as an element in a query using psycopg's sql module.

    Right now a pure clone of Identifier and stores the constructor in the "_wrapped" property

    Note that what we refer to as a "table" may actually be a view or a materialized view, but it queries just like a table
    so for our purposes it's a "table"

    This class also allows us extra features like the ability to get the metadata table if the table is a raw table.
    """


class SchemaTable(sql.Composed):
    """
    A composable instance that takes schema and table strings (or  and allows them to work together

    This subclasses Composed since it involves two idenitifiers linked by the sql.SQL('.') and it
    allows for convenient functionality to abstract away some nuances
    (i.e. like how you must do "schema"."table" as "schema.table" does not work)
    gives you a container object if you ever want to get the schema or the table.

    This class also allows us to get the metadata SchemaTable if appropriate.
    """

    def __init__(self, schema: Union[str, Schema], table: Union[str, Table]):

        if isinstance(schema, Schema):
            self._schema = schema
        elif isinstance(schema, str):
            self._schema = Schema(schema)
        else:
            raise TypeError("schema must be a str or Schema, not a {}".format(type(table)))

        if isinstance(table, Table):
            self._table = table
        elif isinstance(table, str):
            self._table = Table(table)
        else:
            raise TypeError("table must be a str or Table, not a {}".format(type(table)))

        # Store it as a composed of the schema identifier, the table identifier and a period in between
        super().__init__([self._schema, sql.SQL("."), self._table])

    @property
    def string(self) -> str:
        """
        "Returns an unwrapped string version of the schema table for ease of printing
        :return: a string version of the schema table
        """
        return self._schema.string + "." + self._table.string

    @property
    def schema(self) -> Schema:
        """
        Returns a clone of schema (so that it can't be changed)
        :return: a clone of the schema of this SchemaTable
        """
        return Schema(self._schema.string)

    @property
    def table(self) -> Table:
        """
        Returns a clone of table (so that it can't be changed)
        :return: a clone of the table of this SchemaTable
        """
        return Table(self._table.string)


class SQLTypeStruct(sql.Composable):
    """
    A composable instance that takes a postgres sqltype string and allows it to work as an element in a query
    using psycopg's sql module

    This is like the Field / sql.Identifier, except it is even more basic composable that does not put quotes around the
    wrapped input (since SQL Types can't be quoted).

    The goal for this is for use in dynamic CREATE TABLE queries where we give sql types without quotes, and you should
    only construct this by using the class methods
    """

    def as_string(self, context=None):
        """
        Implement the abstract as_string to just give us the string that was given to be wrapped but without quotes.

        This should be safe since we will only use one of the class methods

        :param context: Don't need a context since it won't be quoted
        :return: the string given in the constructor "wrapped" by this class
        """
        return self._wrapped


class SQLType(object):
    """
    An enum container for the SQLTypeStruct's objects.

    In python the only way to make an object return enum-instances of itself is to use class methods which are a bit
    bulky and so easier to just make this second object as the enum object with class properties that reference the
    other object.
    """
    TEXT = SQLTypeStruct("TEXT")
    TEXT_PRIMARY_KEY = SQLTypeStruct("TEXT PRIMARY KEY")
    DATE = SQLTypeStruct("DATE")
    TIMESTAMP = SQLTypeStruct("TIMESTAMP")
    JSONB = SQLTypeStruct("JSONB")
    JSONB_DEFAULT_EMPTY_ARRAY = SQLTypeStruct("JSONB DEFAULT '[]'::json")
    JSONB_DEFAULT_EMPTY_OBJ = SQLTypeStruct("JSONB DEFAULT '{}'::json")
    BOOLEAN = SQLTypeStruct("BOOLEAN")
    BOOLEAN_DEFAULT_TRUE = SQLTypeStruct("BOOLEAN DEFAULT TRUE")
    BOOLEAN_DEFAULT_FALSE = SQLTypeStruct("BOOLEAN DEFAULT FALSE")
    INTEGER = SQLTypeStruct("INTEGER")
    INTEGER_DEFAULT_ZERO = SQLTypeStruct("INTEGER DEFAULT 0")
    DOUBLE_PRECISION = SQLTypeStruct("DOUBLE PRECISION")
    NUMERIC = SQLTypeStruct("NUMERIC")

    @staticmethod
    def NUMERIC_WITH_PRECISION_SCALE(precision: int, scale: int):
        if precision is None or scale is None:
            raise Exception("Must specify either both precision and scale or neither")
        else:
            return SQLTypeStruct("NUMERIC ({}, {})".format(precision, scale))


def get_column_names(schema_table: SchemaTable, cursor: extensions.cursor) -> List[str]:
    """
    Gets a list of all columns (from the information schema) for a given schema and table in the ordinal order

    :param schema_table: the SchemaTable object that we want to get the columns_from
    :param cursor: a cursor for where to execute this query
    :return: a list of all table columns
    """
    schema_name = schema_table.schema.string
    table_name = schema_table.table.string
    cursor.execute("SELECT column_name FROM information_schema.columns "
                   "WHERE table_schema = %s AND table_name = %s ORDER BY ordinal_position",
                   (schema_name, table_name))
    return [x[0] for x in cursor.fetchall()]


def execute_values_insert_query(schema_table: SchemaTable) -> sql.Composable:
    """
    This helper function takes a SchemaTable and creates a generic insert query for use with the execute values method
    (i.e. with the parameter %s following the word values

    :param schema_table: the SchemaTable object to insert
    :return: a Composable wrapper with the insert query
    """
    return sql.SQL("""
          INSERT INTO {} VALUES %s
                    """).format(schema_table)


def get_row_count(schema_table: SchemaTable, cursor: extensions.cursor) -> int:
    """
    Given a SchemaTable and a cursor, this simple utility will run a SELECT COUNT(*) on the object and return an int

    :param schema_table: the SchemaTable object that we want to compute the row count
    :param cursor: a cursor for where to execute this query
    :return: the number of rows in the schema table object after querying the database with the cursor
    """
    cursor.execute(sql.SQL("""
          SELECT COUNT(*) FROM {}
                        """).format(schema_table))
    count = cursor.fetchone()[0]  # grab the first element of the tuple that is returned
    validate_is_int(count)
    return count


def fetch_all_records(schema_table: SchemaTable, cursor: extensions.cursor) -> List:
    """
    Given a SchemaTable and a cursor, this simple utility will run a SELECT * on the object and return the full thing in
    memory. Recommended for use only on small objects!

    :param schema_table: the SchemaTable object that we want to fetch all from
    :param cursor: a cursor for where to execute this query
    :return: a list of tuple records with the table in memory
    """
    cursor.execute(sql.SQL("""
          SELECT * FROM {}
                        """).format(schema_table))
    return cursor.fetchall()


def get_column_count(schema_table: SchemaTable, cursor: extensions.cursor) -> int:
    """
    Given a SchemaTable and a cursor, this simple utility will query the information schema to find out how many
    columns are in it.

    Note that this works equally well if the schema_table actually refers to a view, but it won't work with a
    materialized view since they aren't part of the SQL standard (so they aren't in the information schema)

    :param schema_table: the SchemaTable object that we want to compute the row count
    :param cursor: a cursor for where to execute this query
    :return: the number of rows in the schema table object after querying the database with hte cursor
    """
    schema_name = schema_table.schema.string
    table_name = schema_table.table.string

    cursor.execute(sql.SQL("""
          SELECT COUNT(*) FROM information_schema.columns 
          WHERE table_schema = %s AND table_name = %s
                        """), (schema_name, table_name))
    count = cursor.fetchone()[0]  # grab the first element of the tuple that is returned
    validate_is_int(count)
    return count


def get_list_field_type_tuples(schema_table: SchemaTable, cursor: extensions.cursor) -> List[Tuple[str, str]]:
    """
    Takes a schema table and a cursor and returns a list of tuples with the str field
    name and the sqltype in the proper ordinal order (which it gets by querying the information_schema).

    Note that the type is simply whatever is in the data_type field, and as of now, this does not use the precision
    and scale for numeric types.

    Note that this works equally well if the schema_table actually refers to a view, but it won't work with a
    materialized view since they aren't part of the SQL standard (so they aren't in the information schema)

    :param schema_table: the schema table to use (can also be views, but not materialized views)
    :param cursor: the cursor for where to execute this query
    :return: a list of tuple of strings, each one containing the field name and the sql type in ordinal order
    """
    schema_name = schema_table.schema.string
    table_name = schema_table.table.string

    cursor.execute(sql.SQL("""
            SELECT column_name, data_type FROM information_schema.columns
            WHERE table_schema = %s AND table_name = %s ORDER BY ordinal_position
              """), (schema_name, table_name))

    # TODO add precision and scale to a parenthetical for numeric types
    # TODO make this return List[Tuple[Field, SQLType] instead of List[str, str]
    return cursor.fetchall()


def create_table_from_field_sql_type_tuples(schema_table: SchemaTable,
                                            list_field_type_tuples: List[Tuple[Field, SQLType]]) -> sql.Composable:
    """
    Takes a schema table and a list of (Field, SQLType) tuples and returns a create table SQL Composable.

    :param schema_table: the schema table to use to make the table
    :param list_field_type_tuples: a list of tuples, each containing the field name and the sql type in ordinal order
    """

    list_field_type_sql = [sql.SQL("{field}\t\t{type}").format(field=x[0], type=x[1])
                           for x in list_field_type_tuples]

    return sql.SQL("CREATE TABLE {schema_table} (\n\t{field_types_joined}\n);"
                   "").format(schema_table=schema_table,
                              field_types_joined=sql.SQL(",\n\t").join(list_field_type_sql))


def upsert_sql_from_field_value_dict(schema_table: SchemaTable, field_value_dict: Dict[Field, Any],
                                     conflict_field_list: List[Field]) -> sql.Composable:
    """
    Takes a schema table, a dict mapping Fields to values, and a list of fields to check for conflicts on and creates
    and "upsert", meaning that we will try to insert the dict values associated with each field key into the table,
    and if that fails due to a conflict where the conf;ict field lists already exist, then do an update instead.

    Also we run lstrip and rstrip on any string that is a value.

    :param schema_table: the schema table to upsert into
    :param field_value_dict: the dict mapping a Field to a value representing the data we want to upsert
    :param conflict_field_list: a list of fields to use for the on conflict column – note that this is often a single
    field serving as the primary key but multiple fields for composite keys are inserted
    :return: a list
    """

    # Grab the fields and values (the order will be preserved by grabbing these without changing the dict in between)
    field_list = field_value_dict.keys()

    # Strip whitespace with rstrip and lstrip if a string (i.e. something that has lstrip and rstrip)
    val_list = []
    for x in field_value_dict.values():
        if hasattr(x, 'rstrip') and hasattr(x, 'lstrip'):
            x = x.rstrip().lstrip()
        val_list.append(x)

    field_value_dict.values()
    val_list = [sql.Literal(x) for x in val_list]  # Convert the values into sql.Literal for insertion

    # EXCLUDED is the posgres name of the records that couldn't be inserted due to the conflict
    exc_fields = [sql.SQL("EXCLUDED.{}").format(x) for x in field_list]

    if len(field_list) == 0:
        raise Exception("Cannot do upsert with an empty field_value_dict!")

    # The necessity of these two templates is due to an annoying discrepancy between Postgres 9 and Postgres 10:
    # The SQL without the the parentheses works for Postgres 9 for all cases, but fails in 10 if you have only one field
    # because 10 wants you to insert the keyword ROW before the parentheses since ROW(1) ≠ (1).
    # Inserting this keyword would fix the parentheses version in 10 but the ROW keyword is not supported in 9.

    # So the solution is to remove the parentheses if the field list is length 1 and keep them if the field list is
    # longer than 1 (which works on both 9 and 10!)
    if len(field_list) == 1:
        upsert_sql_template = sql.SQL("INSERT INTO {schema_table} ({joined_fields}) VALUES ({joined_vals}) \n"
                                      "ON CONFLICT ({joined_conf_fields}) \n"
                                      " DO UPDATE SET {joined_fields} = {joined_exc_fields};")

    else:  # This is the only one necessary in 9 but breaks in 10 if you have only one field
        upsert_sql_template = sql.SQL("INSERT INTO {schema_table} ({joined_fields}) VALUES ({joined_vals}) \n"
                                      "ON CONFLICT ({joined_conf_fields}) \n"
                                      " DO UPDATE SET ({joined_fields}) = ({joined_exc_fields});")

    return upsert_sql_template.format(
        schema_table=schema_table,
        joined_fields=sql.SQL(", ").join(field_list),
        joined_vals=sql.SQL(", ").join(val_list),
        joined_conf_fields=sql.SQL(", ").join(conflict_field_list),
        joined_exc_fields=sql.SQL(", ").join(exc_fields)
    )


class TableError(Exception):
    """
    An exception for when the table given as an argument is not as expected
    """
    pass


if __name__ == '__main__':
    with LocalhostCursor(dict_cursor=True) as cur:
        pass

