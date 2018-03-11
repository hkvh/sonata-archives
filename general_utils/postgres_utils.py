#!/usr/bin/env python
import copy
import json
import logging
from abc import ABCMeta, abstractmethod
from typing import Dict, Any, Union

from psycopg2 import pool, extensions, extras
from psycopg2._psycopg import AsIs
from psycopg2.extensions import register_adapter

from credentials import pg_localhost
from database_design.key_enums import KeyStruct

log = logging.getLogger(__name__)


# Create a new JSON class that will try to use __str__ to serialize all object as JSON
class StringConverterJSON(extras.Json):
    def dumps(self, obj):
        """
        Overwrites the normal dumping of an object into a JSON for psycopg2 to try to use the str(x) to coaxe objects
        to tbe JSON serializable instead of throwing a type error

        :param obj: the object to convert
        :return: the json representation
        """
        try:
            return json.dumps(obj)
        except TypeError:
            if isinstance(obj, list):
                return json.dumps([str(x) for x in obj])
            elif isinstance(obj, dict):
                return json.dumps({str(k): str(v) for k, v in obj.items()})


# This allows us to directly commit dict and list objects as JSONB with psycopg2
register_adapter(dict, StringConverterJSON)
register_adapter(list, StringConverterJSON)

# We also want our KeyStruct to be adapted as a normal text string so we can insert it directly as text
register_adapter(KeyStruct, lambda x: AsIs("'{}'".format(str(x))))


class PostgresConnectionManager(object):
    """
    A class that stores and manages a psycopg2 connection pool for a postgres database.

    Right now, the class just wraps the SimpleConnectionPool, but in the future could do something more complicated.
    """

    def __init__(self, conn_name, minconn=1, maxconn=5, **kwargs):
        """
        Instantiates a Simple Connection Pool object with minconn and maxconn

        :param conn_name: What to name this connection
        :param minconn: The minimum number of connections created
        :param maxconn: The maximum number of connections possible
        :param kwargs: A set of named parameters which should be passed in to set up the connection pool (i.e.
        user, password, host, port, database)
        """
        self._conn_pool = pool.SimpleConnectionPool(minconn=minconn, maxconn=maxconn, **kwargs)
        self.num_utilized_conns = 0
        self.max_num_conns = maxconn
        self.conn_name = conn_name

    def get_connection(self) -> extensions.connection:
        """
        Gets an available connection from the database
        :return: the connection
        """
        self.num_utilized_conns = self.num_utilized_conns + 1
        # log.debug("{} Connection requested;  \t\tproposed num in use: {} / {}"
        #           "".format(self.conn_name, self.num_utilized_conns, self.max_num_conns))
        return self._conn_pool.getconn()

    def return_connection(self, conn: extensions.connection) -> None:
        """
        Returns a connection back to the pool
        :param conn: the connection to return
        """
        self._conn_pool.putconn(conn)
        self.num_utilized_conns = self.num_utilized_conns - 1
        # log.debug("{} Connection returned;  \t\tcurrent num in use: {} / {}"
        #           "".format(self.conn_name, self.num_utilized_conns, self.max_num_conns))


class PostgresCursor(object, metaclass=ABCMeta):
    """
    An abstract class for use in a "with" construct to get a psycopg2 cursor that can be used to execute queries.

    By using it with the with construct, we no longer have to worry about closing the cursor, returning the
    connection back to the connection pool, or committing the connection's changes.

    Concrete subclasses of this class will simply implement the credentials_dict() that will be used to generate a
    connection manager for the Postgres database and then the concrete class can be instantiated in the with clause
    every time we need a cursor to that database.

    For example, with a subclass like LocalhostCursor() that simply implements credentials_dict(), all we need to do is:

    with LocalhostCursor() as cur:
        cur.execute("<SQL>")
    """

    _global_conn_manager = None  # type: Union[PostgresConnectionManager, None]

    @staticmethod
    @abstractmethod
    def credentials_dict() -> Dict[str, Any]:
        """
        Returns the credentials dict that this cursor is going to enable us to query
        :return: a dictionary containing all named parameters we need to connect
        (i.e. user, password, host, port, database)
        """

    @staticmethod
    @abstractmethod
    def pg_db_display_name() -> str:
        """
        Returns the name of this database (for use in logging)

        :return: the string name of our database we are connecting to
        """

    @classmethod
    def get_connection_manager(cls) -> PostgresConnectionManager:
        """
        Gets the connection_manager by either returning the class _global_conn_manager if it exists or creating it
        based on the credentials_dict and returning it after caching it in _global_conn_manager.

        (This is essentially a wrapper method that uses the singleton pattern to prevent the costly operation of
        opening up a connection)
        """

        if cls._global_conn_manager is None:
            # Create the connection manager by passing in the unpacked credentials_dict
            conn_manager = PostgresConnectionManager(cls.pg_db_display_name(), **cls.credentials_dict())

            # Log the success method but hide the password
            credentials_dict_copy = copy.deepcopy(cls.credentials_dict())
            credentials_dict_copy['password'] = "******"
            log.info("Connection to Postgres was successful: {}".format(
                credentials_dict_copy))

            # Save it so we never have to remake it again
            cls._global_conn_manager = conn_manager
        else:
            conn_manager = cls._global_conn_manager
        return conn_manager

    def __init__(self, dict_cursor: bool = False, server_side_named_cursor: bool = False):
        """
        Creates an instance with a connection manager, and uses it to grab a connection and then a cursor.

        Runs the class method get_connection_manager() that will make the connection manager if it can't find it
        in the class global

        :param dict_cursor: defaults to False, but if True, will make the cursor be usable as a dict instead of
        the usual tuple cursor
        :param server_side_named_cursor: defaults to False, but if True will make the cursor have a name and thus be a
        server side named cursor that is more limited (only designed for large select statements)
        """
        self.conn_manager = self.get_connection_manager()
        self.conn = self.conn_manager.get_connection()
        self._cursor = self.conn.cursor(name='server' if server_side_named_cursor else None,
                                        cursor_factory=extras.DictCursor if dict_cursor else None)
        # psycopg2 stupidly doesn't type hint the cursor() method so I'm going to wrap it with my own property
        # This way auto-complete will work with self.cursor

    @property
    def cursor(self) -> extensions.cursor:
        """
        A wrapper for self._cursor that enables type hinting. (This is because psycopg2 stupidly doesn't type hint
        the connection's cursor() method)

        :return: the cursor
        """
        return self._cursor

    def __enter__(self) -> extensions.cursor:
        """
        The code that will execute at the beginning of the "with" clause.

        :return: A cursor that will be assigned to whatever variable is used with "as"
        """
        return self.cursor

    def __exit__(self, exception_type, exception_value, exception_traceback):
        """
        The tear-down code that will execute at the end of the with statement regardless of errors.

        If there were no errors need to close the cursor, commit to the database and return the connection
        If there were errors, let's rollback

        :param exception_type: the type of exception
        :param exception_value: the value of the exception
        :param exception_traceback: the exception traceback
        """
        self.cursor.close()
        if exception_value is not None:
            log.error(
                "Error of type {} with value \"{}\" occurred in a with block involving the cursor, rolling back, "
                "and not committing anything.".format(
                    exception_type,
                    exception_value))
            self.conn.rollback()
        else:
            # log.debug("Committing changes from the connection and returning it to the Connection Manager")
            self.conn.commit()
        self.conn_manager.return_connection(self.conn)


class LocalhostCursor(PostgresCursor):
    """
    A PostgresCursor for connection to a localhost pg instance using the credentials.py file
    """

    @staticmethod
    def pg_db_display_name() -> str:
        return "postgres"

    @staticmethod
    def credentials_dict() -> Dict[str, Any]:
        return pg_localhost


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)s %(levelname)s: %(message)s')
