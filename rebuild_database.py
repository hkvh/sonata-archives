#!/usr/bin/env python
"""
A module designed to rebuild the entire database from the database_design and fill it with data
"""
import glob
import importlib
import logging
import os
import types

from psycopg2 import extensions, sql

from database_design.sonata_table_specs import Composer, Piece, Sonata, Introduction, Exposition, Development, \
    Recapitulation, Coda, sonata_archives_schema
from directories import DATA_DIR, ROOT_DIR
from general_utils.postgres_utils import LocalhostCursor

log = logging.getLogger(__name__)

# The function we assume all data modules will have
DATA_MODULE_UPSERT_ALL = 'upsert_all'
COMPOSERS_FILE_NAME = 'composers.py'


def create_all_tables(cur: extensions.cursor, drop_if_exists: bool = True) -> None:
    """
    This function creates all sonata tables needed to construct the sonata_archives

    :param cur: a cursor for which to execute this statement
    :param drop_if_exists: if true, will wipe out the existing tables and rebuild
    """

    log.info('#' * 40)
    log.info('#' * 40)
    log.info("CREATING ALL TABLES")
    log.info('#' * 40)
    log.info('#' * 40)

    # Create sonata archives schema
    create_schema_sql = sql.SQL("CREATE SCHEMA IF NOT EXISTS {s};").format(s=sonata_archives_schema)
    log.info("\n\n" + create_schema_sql.as_string(cur) + "\n")
    cur.execute(create_schema_sql)

    # Loop over all objects twice to both create them and add their constraints
    sonata_table_specs = [
        Composer,
        Piece,
        Introduction,
        Exposition,
        Development,
        Recapitulation,
        Coda,
        Sonata,  # Sonata objects contain FKs to all the blocks so the block PKs must be created first
    ]
    for table in sonata_table_specs:
        create_table_sql = table.create_table_sql(drop_if_exists)
        log.info("\n\n" + create_table_sql.as_string(cur) + "\n")
        cur.execute(create_table_sql)

    # Execute constrain sql only after making all tables
    for table in sonata_table_specs:
        create_constraint_sql = table.create_constraints_sql()
        log.info("\n" + create_constraint_sql.as_string(cur) + "\n")
        cur.execute(create_constraint_sql)


def upsert_all_data(cur: extensions.cursor, fail_if_data_module_missing_upsert_all=True) -> None:
    """
    This function recursively iterates over all files in the 'data' folder and grabs and runs their "upsert_all"
    function. Every data class must contain an upsert_all method or this will ignore the module or throw an exception
    (depending on the choice of fail_if_data_module_missing_upsert_all)

    :param cur: a cursor for which to execute this statement
    :param fail_if_data_module_missing_upsert_all: if True we throw an exception, if False we ignore the module
    """

    # Get all python files recursively under the data dir
    data_file_full_path_list = glob.glob(os.path.join(DATA_DIR, '**/*.py'), recursive=True)

    log.info('#' * 40)
    log.info('#' * 40)
    log.info("UPSERTING ALL DATA")
    log.info('#' * 40)
    log.info('#' * 40 + "\n")

    first = True
    for data_file_full_path in data_file_full_path_list:

        path_name, file_name = os.path.split(data_file_full_path)

        # Skip any module specifier files as they don't count
        if file_name == '__init__.py':
            continue

        # Make sure that composers is always first since we need that module upserted first
        # (because it's the only file at root level, it should be, but let's check just in case)
        if first and file_name != COMPOSERS_FILE_NAME:
            raise Exception("Encountered file {0} before {1}... "
                            "Make sure {1} is the only file in the root data directory so it is executed first!"
                            "".format(file_name, COMPOSERS_FILE_NAME))
        first = False

        data_module = get_module_from_data_dirname(data_file_full_path)

        log.info('#' * 150)
        log.info("LOADED: {}".format(data_module))
        log.info('#' * 150)

        # If we have the attribute, call it after making sure it's a function
        if hasattr(data_module, DATA_MODULE_UPSERT_ALL):
            log.info("CALLING '{}':\n".format(DATA_MODULE_UPSERT_ALL))
            upsert_func = getattr(data_module, DATA_MODULE_UPSERT_ALL)

            # If it's not a function... that's weird and we always want that to fail everything
            if not isinstance(upsert_func, types.FunctionType):
                raise TypeError("{} contained '{}' but it wasn't a function!".format(data_module,
                                                                                     DATA_MODULE_UPSERT_ALL))
            upsert_func()

        # Otherwise ignore it or raise an error depending on the option
        else:
            log.info("Module is missing function '{}':".format(DATA_MODULE_UPSERT_ALL))
            if not fail_if_data_module_missing_upsert_all:
                log.info("Ignoring it...\n")
                continue
            else:
                raise Exception("{} missing function '{}':".format(data_module, DATA_MODULE_UPSERT_ALL))


def get_module_from_data_dirname(data_file_full_path: str):
    """
    Given a full path from a data file, this method will convert it into a module imported by the importlib by stripping
    it down to just the elements beyond the root dir and then joining them with '.'

    :param data_file_full_path: the string name of the full path
    :return: the data file as a module
    """
    module_element_list = []

    # Pop the last element off the full path until we reach the ROOT_DIR
    path = data_file_full_path
    while True:
        # If path is ROOT_DIR, we have everything
        if path == ROOT_DIR:
            break
        elif path == "":
            raise Exception(
                "Error! Root directory {} not present at the base of path {}".format(ROOT_DIR, data_file_full_path))

        # Pop off the last element and extension and insert it at the beginning of the list
        path, last = os.path.split(path)
        last = os.path.splitext(last)[0]   # remove extension

        # insert at the beginning since last element popped is actually the earliest dir
        module_element_list.insert(0, last)

    module_name = '.'.join(module_element_list)
    module = importlib.import_module(module_name)
    return module


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)s %(levelname)s: %(message)s')

    with LocalhostCursor() as cur:
        create_all_tables(cur, drop_if_exists=True)

    # Need to leave the with block to commit the connection so that the tables exist
    with LocalhostCursor() as cur:
        upsert_all_data(cur, fail_if_data_module_missing_upsert_all=False)
