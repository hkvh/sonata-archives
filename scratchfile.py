#!/usr/bin/env python
from database_design.sonata_table_specs import Expo
from database_design.sonata_view_specs import ExpositionRecapitulation
from general_utils.sql_utils import *

with LocalhostCursor() as cur:
    # print(get_column_names(Exposition.schema_table(), cur))
    print(ExpositionRecapitulation.create_view_sql(cur).as_string(cur))