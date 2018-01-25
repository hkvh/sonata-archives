#!/usr/bin/env python
"""
A module designed to utilize the sonata_table_specs to build the sonata table
"""
import logging
from psycopg2 import extensions, sql

from database_design.sonata_table_specs import Composer, Piece, Sonata, Introduction, Exposition, Development, \
    Recapitulation, Coda, sonata_archives_schema
from general_utils.postgres_utils import LocalhostCursor

log = logging.getLogger(__name__)


def create_all_sonata_tables(cur: extensions.cursor, drop_if_exists: bool = True) -> None:
    """
    This function creates all sonata tables needed for the archives

    :param cur: a cursor for which to execute this statement
    :param drop_if_exists: if true, will wipe out the existing tables and rebuild
    """

    # Create sonata archives schema
    create_schema_sql = sql.SQL("CREATE SCHEMA IF NOT EXISTS {s};").format(s=sonata_archives_schema)
    log.info("\n\n" + create_schema_sql.as_string(cur) + "\n")
    cur.execute(create_schema_sql)

    # Loop over all objects twice to both create them and add their constraints
    sonata_table_specs = [
        Composer,
        Piece,
        Sonata,
        Introduction,
        Exposition,
        Development,
        Recapitulation,
        Coda,
    ]
    for table in sonata_table_specs:
        create_table_sql = table.create_table_sql(drop_if_exists)
        log.info("\n\n" + create_table_sql.as_string(cur) + "\n")
        cur.execute(create_table_sql)

    # Execute constrain sql only after making all tables
    for table in sonata_table_specs:
        create_constraint_sql = table.create_constraints_sql()
        log.info("\n\n" + create_constraint_sql.as_string(cur) + "\n")
        cur.execute(create_constraint_sql)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)s %(levelname)s: %(message)s')

    with LocalhostCursor() as cur:
        create_all_sonata_tables(cur, drop_if_exists=True)
