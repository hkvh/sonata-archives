#!/usr/bin/env python
"""
A module containing the specification for the base SQL tables (and views, which act like tables)
"""

from psycopg2 import sql, extensions

from database_design.sonata_table_specs import sonata_archives_schema, Exposition, Recapitulation
from database_design.view_spec import ViewSpecification
from general_utils.sql_utils import SchemaTable, Field, get_column_names


class ExpositionRecapitulation(ViewSpecification):
    """
    The view that shows all data in all common columns between the Exposition and Recapitulation.

    (Since Recap Table Spec inherits from Exposition we just need to query all Exposition columns
    """

    @classmethod
    def schema_table(cls) -> SchemaTable:
        return SchemaTable(sonata_archives_schema, "exposition_recapitulation")

    @classmethod
    def view_select_sql(cls, cur: extensions.cursor) -> sql.Composable:

        # Grab all exposition fields and cast them as a field list
        all_expo_fields_list = [Field(x) for x in get_column_names(Exposition.schema_table(), cur)]

        # Note: since the id of exposition is _e and recap is _r, ordering by id will give us expo before recap
        # for all sonatas (which is what we want)
        return sql.SQL("""
            SELECT {all_expo_fields} 
            FROM {expo_st}
            UNION
            SELECT {all_expo_fields}
            FROM {recap_st}
            ORDER BY {id};
        """).format(all_expo_fields=sql.SQL(',').join(all_expo_fields_list),
                    expo_st=Exposition.schema_table(),
                    recap_st=Recapitulation.schema_table(),
                    id=Exposition.ID)
