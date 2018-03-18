#!/usr/bin/env python
"""
A module containing the specification for the base SQL tables (and views, which act like tables)
"""
from abc import abstractmethod
from typing import Tuple, List, Set, Any, Dict

from psycopg2 import sql, extensions

from database_design.table_spec import TableSpecification
from general_utils.sql_utils import Field, SQLType, SchemaTable, Schema

sonata_archives_schema = Schema("sonata_archives")


class ColumnDisplay(TableSpecification):
    """
    The table that stores the information about how to map all other tables raw fields to display name
    """

    @classmethod
    def schema_table(cls) -> SchemaTable:
        return SchemaTable(sonata_archives_schema, "column_display")

    TABLE_NAME = Field("table_name")
    COLUMN_NAME = Field("column_name")
    DISPLAY_NAME = Field("display_name")

    @classmethod
    def field_sql_type_list(cls) -> List[Tuple[Field, SQLType]]:
        return [
            (cls.TABLE_NAME, SQLType.TEXT),
            (cls.COLUMN_NAME, SQLType.TEXT),
            (cls.DISPLAY_NAME, SQLType.TEXT),
        ]

    @classmethod
    def create_constraints_sql(cls) -> sql.Composable:
        # Add a compound key since every table + column combo is unique
        return sql.SQL("ALTER TABLE {st} ADD PRIMARY KEY ({tn}, {cn});").format(st=cls.schema_table(),
                                                                                tn=cls.TABLE_NAME,
                                                                                cn=cls.COLUMN_NAME)

    @classmethod
    def create_new_dict_with_display_name_keys(cls, cursor: extensions.cursor, table_name: str,
                                               dict_with_column_name_keys: Dict[str, Any]) -> Dict[str, Any]:
        """
        Given a table_name and a dict with keys serving as raw column names, this method will query the Column
        Display table to return a new dict with the the keys replaced with display names (values remain the same)

        :param cursor: the cursor to use to execute this query
        :param table_name: the name of the table that these column name keys refer to
        :param dict_with_column_name_keys: a dict with column raw names as keys
        :return: a clone of the above dict with all keys replaced by the original key's corresponding display name
        """

        select_query = sql.SQL("""
              SELECT {cn}, {dn} 
              FROM {st} 
              WHERE {tn} = {tn_val};
        """).format(st=cls.schema_table(),
                    cn=cls.COLUMN_NAME,
                    dn=cls.DISPLAY_NAME,
                    tn=cls.TABLE_NAME,
                    tn_val=sql.Literal(table_name))

        cursor.execute(select_query)

        raw_display_map = {raw: display for raw, display in cursor.fetchall()}
        try:
            dict_with_display_name_keys = {raw_display_map[key]: value
                                           for key, value in dict_with_column_name_keys.items()}
        except KeyError as e:
            raise KeyError("{} was not in raw_display_map which looks like this: {}".format(e, raw_display_map))

        return dict_with_display_name_keys


class Composer(TableSpecification):
    """
    The table that stores information about composers
    """

    @classmethod
    def schema_table(cls) -> SchemaTable:
        return SchemaTable(sonata_archives_schema, "composer")

    ID = Field("id")
    FULL_NAME = Field("full_name", "Full Name")
    SURNAME = Field("surname", "Surname")
    NATIONALITY = Field("nationality", "Nationality")
    BIRTH_DATE = Field("birth_date", "Birth Date")
    DEATH_DATE = Field("death_date", "Death Date")
    BIRTHPLACE = Field("birthplace", "Birthplace")
    PRIMARY_RESIDENCE = Field("primary_residence", "Primary Residence")

    @classmethod
    def field_sql_type_list(cls) -> List[Tuple[Field, SQLType]]:
        return [
            (cls.ID, SQLType.TEXT),
            (cls.FULL_NAME, SQLType.TEXT),
            (cls.SURNAME, SQLType.TEXT),
            (cls.NATIONALITY, SQLType.TEXT),
            (cls.BIRTH_DATE, SQLType.DATE),
            (cls.DEATH_DATE, SQLType.DATE),
            (cls.BIRTHPLACE, SQLType.TEXT),
            (cls.PRIMARY_RESIDENCE, SQLType.TEXT),
        ]

    @classmethod
    def create_constraints_sql(cls) -> sql.Composable:
        return sql.SQL("ALTER TABLE {st} ADD PRIMARY KEY ({id});").format(st=cls.schema_table(),
                                                                          id=cls.ID)


class Piece(TableSpecification):
    """
    The table that stores information about pieces that contain sonatas.

    Links to the composer table - so if using create_constraints_sql, that table must exist first!
    """

    @classmethod
    def schema_table(cls) -> SchemaTable:
        return SchemaTable(sonata_archives_schema, "piece")

    ID = Field("id")
    COMPOSER_ID = Field("composer_id")
    NAME = Field("name", "Piece Name")
    CATALOGUE_ID = Field("catalogue_id",
                         "Catalogue Number")  # K. for mozart, D. for schubert, Op. and No. for most composers
    NICKNAME = Field("nickname", "Piece Nickname")
    FULL_NAME = Field("full_name",
                      "Piece Full Name")  # usually don't enter this, let it be derived from name, cat_id and nickname
    PIECE_TYPE = Field("piece_type", "Piece Type")  # Symphony vs. Piano Sonata etc.
    YEAR_STARTED = Field("year_started", "Year Started")
    YEAR_COMPLETED = Field("year_completed", "Year Completed")
    PREMIER_DATE = Field("premier_date", "Premier Date")
    GLOBAL_KEY = Field("global_key", "Global Key")
    NUM_MOVEMENTS = Field("num_movements", "Movements")

    @classmethod
    def field_sql_type_list(cls) -> List[Tuple[Field, SQLType]]:
        return [
            (cls.ID, SQLType.TEXT),
            (cls.COMPOSER_ID, SQLType.TEXT),
            (cls.NAME, SQLType.TEXT),
            (cls.CATALOGUE_ID, SQLType.TEXT),
            (cls.NICKNAME, SQLType.TEXT),
            (cls.FULL_NAME, SQLType.TEXT),
            (cls.PIECE_TYPE, SQLType.TEXT),
            (cls.YEAR_STARTED, SQLType.INTEGER),
            (cls.YEAR_COMPLETED, SQLType.INTEGER),
            (cls.PREMIER_DATE, SQLType.DATE),
            (cls.GLOBAL_KEY, SQLType.TEXT),
            (cls.NUM_MOVEMENTS, SQLType.INTEGER),
        ]

    @classmethod
    def create_constraints_sql(cls) -> sql.Composable:
        return sql.SQL("ALTER TABLE {st} ADD PRIMARY KEY ({id});\n"
                       "ALTER TABLE {st} ADD FOREIGN KEY ({comp_id}) REFERENCES {c_st}({c_id});") \
            .format(st=cls.schema_table(), id=cls.ID, comp_id=cls.COMPOSER_ID,
                    c_st=Composer.schema_table(), c_id=Composer.ID)


class Sonata(TableSpecification):
    """
    The core sonata table with information about the sonata.

    Links to the piece table and the sonata block tables - so if using create_constraints_sql,
    those tables must exist first!
    """

    @classmethod
    def schema_table(cls) -> SchemaTable:
        return SchemaTable(sonata_archives_schema, "sonata")

    ID = Field("id")
    PIECE_ID = Field("piece_id")
    MOVEMENT_NUM = Field("movement_num", "Movement")
    SONATA_TYPE = Field("sonata_type", "Sonata Type")  # Sonata Theory Types 1-5
    GLOBAL_KEY = Field("global_key", "Sonata Global Key")
    MEASURE_COUNT = Field("measure_count", "Sonata Measure Count")
    EXPOSITION_REPEAT = Field("exposition_repeat", "Exposition Repeat")
    DEVELOPMENT_RECAP_REPEAT = Field("development_recap_repeat", "Development/Recap Repeat")
    INTRODUCTION_PRESENT = Field("introduction_present", "Introduction Present")
    DEVELOPMENT_PRESENT = Field("development_present", "Development Present")
    CODA_PRESENT = Field("coda_present", "Coda Present")
    INTRODUCTION_ID = Field("introduction_id")
    EXPOSITION_ID = Field("exposition_id")
    DEVELOPMENT_ID = Field("development_id")
    RECAPITULATION_ID = Field("recapitulation_id")
    CODA_ID = Field("coda_id")
    LILYPOND_IMAGE_SETTINGS = Field("lilypond_image_settings")  # Contains properties about the image for display

    # The keys for use in the image settings dict / JSON
    IMAGE_WIDTH = "image_width"
    IMAGE_PATH = "image_path"

    @classmethod
    def field_sql_type_list(cls) -> List[Tuple[Field, SQLType]]:
        return [
            (cls.ID, SQLType.TEXT),
            (cls.PIECE_ID, SQLType.TEXT),
            (cls.MOVEMENT_NUM, SQLType.INTEGER),
            (cls.SONATA_TYPE, SQLType.TEXT),
            (cls.GLOBAL_KEY, SQLType.TEXT),
            (cls.MEASURE_COUNT, SQLType.INTEGER),
            (cls.EXPOSITION_REPEAT, SQLType.BOOLEAN_DEFAULT_TRUE),
            (cls.DEVELOPMENT_RECAP_REPEAT, SQLType.BOOLEAN_DEFAULT_FALSE),
            (cls.INTRODUCTION_PRESENT, SQLType.BOOLEAN_DEFAULT_FALSE),
            (cls.DEVELOPMENT_PRESENT, SQLType.BOOLEAN_DEFAULT_TRUE),
            (cls.CODA_PRESENT, SQLType.BOOLEAN_DEFAULT_FALSE),
            (cls.INTRODUCTION_ID, SQLType.TEXT),
            (cls.EXPOSITION_ID, SQLType.TEXT),
            (cls.DEVELOPMENT_ID, SQLType.TEXT),
            (cls.RECAPITULATION_ID, SQLType.TEXT),
            (cls.CODA_ID, SQLType.TEXT),
            (cls.LILYPOND_IMAGE_SETTINGS, SQLType.JSONB)
        ]

    @classmethod
    def create_constraints_sql(cls) -> sql.Composable:
        # Add ON DELETE CASCADE to the FK for the blocks so that if we delete a block it deletes the sonata
        # We are going to upsert the sonata at the end of adding all the blocks anyway, so this is just easier
        # to ensure that you clear its FK link to any block that has been deleted
        return sql.SQL("ALTER TABLE {st} ADD PRIMARY KEY ({id});\n"
                       "ALTER TABLE {st} ADD FOREIGN KEY ({piece_id}) REFERENCES {p_st}({p_id});\n"
                       "ALTER TABLE {st} ADD FOREIGN KEY ({intro_id}) REFERENCES {i_st}({i_id}) ON DELETE CASCADE;\n"
                       "ALTER TABLE {st} ADD FOREIGN KEY ({expo_id}) REFERENCES {e_st}({e_id}) ON DELETE CASCADE;\n"
                       "ALTER TABLE {st} ADD FOREIGN KEY ({devel_id}) REFERENCES {d_st}({d_id}) ON DELETE CASCADE;\n"
                       "ALTER TABLE {st} ADD FOREIGN KEY ({recap_id}) REFERENCES {r_st}({r_id}) ON DELETE CASCADE;\n"
                       "ALTER TABLE {st} ADD FOREIGN KEY ({coda_id}) REFERENCES {c_st}({c_id}) ON DELETE CASCADE;") \
            .format(st=cls.schema_table(), id=cls.ID,
                    piece_id=cls.PIECE_ID, p_st=Piece.schema_table(), p_id=Piece.ID,
                    intro_id=cls.INTRODUCTION_ID, i_st=Introduction.schema_table(), i_id=Piece.ID,
                    expo_id=cls.EXPOSITION_ID, e_st=Exposition.schema_table(), e_id=Piece.ID,
                    devel_id=cls.DEVELOPMENT_ID, d_st=Development.schema_table(), d_id=Piece.ID,
                    recap_id=cls.RECAPITULATION_ID, r_st=Recapitulation.schema_table(), r_id=Piece.ID,
                    coda_id=cls.CODA_ID, c_st=Coda.schema_table(), c_id=Piece.ID)


class SonataBlockTableSpecification(TableSpecification):
    """
    An ABC Table Specification for a sonata block that contains some additional functionality that will be shared
    across each of the sonata blocks
    """

    # All blocks must have the same ID column
    ID = Field("id")

    @staticmethod
    def get_relative_from_absolute(absolute_key_field: Field) -> Field:
        """
        Given a field name with the word 'key' implying absolute, dynamically replaces it with 'relative key'.

        :param absolute_key_field: the name of the absolute key field. Must contain the word "key"
        :return: a new Field with key switched out for relative key as its name
        """
        name = absolute_key_field.name
        display_name = absolute_key_field.display_name

        if 'key' not in name or 'Key' not in display_name:
            raise Exception("Field {} with display_name {} marked as an absolute key field but didn't contain \"key\" "
                            "in its name or \"Key\" in its display name!".format(name, display_name))
        else:
            return Field(name.replace('key', 'relative_key'), display_name=display_name.replace('Key', 'Relative Key'))

    @classmethod
    @abstractmethod
    def absolute_key_fields(cls) -> Set[Field]:
        """
        Returns a set of all absolute key fields, which will be the set of fields for which we will add a
        corresponding relative key.

        :return: a set of fields corresponding to all the fields that are for absolute keys
        """

    @staticmethod
    def get_measure_count_from_measure_range(measure_range_field: Field) -> Field:
        """
        Given a field name with the word 'measures', dynamically replaces it with 'measure count.

        :param measure_range_field: the name of the measure range. Must contain the word "measures"
        :return: a new Field with 'measures' switched out for 'measure count as its name
        """
        name = measure_range_field.name
        display_name = measure_range_field.display_name

        if 'measures' not in name or ('Measures' not in display_name and 'Measure(s)' not in display_name):
            raise Exception("Field {} with display_name {} marked as a MeasureRange but didn't contain \"measures\" "
                            "in its name or \"Measures\" in its display name!".format(name, display_name))
        else:
            return Field(name.replace('measures', 'measure_count'),
                         display_name=display_name.replace('Measures', 'Measure Count'))

    @classmethod
    @abstractmethod
    def measure_range_fields(cls) -> Set[Field]:
        """
        Returns a set of all measure range fields, which will be the set of fields for which we will add a
        corresponding measure counts.

        :return: a set of fields corresponding to all the fields that are for measure ranges.
        """

    @classmethod
    @abstractmethod
    def field_sql_type_list_pre_derived_fields(cls) -> List[Tuple[Field, SQLType]]:
        """
        Since we override field_sql_type_list in this class to compute derived fields, this is the method that
        subclasses implement instead, which we now make clear is for before the derived fields

        :return: a list of tuple pairs of fields with their sql type in the ordinal order that we want them in the table
        Any derived fields will change this order, however
        """

    @classmethod
    def field_sql_type_list(cls) -> List[Tuple[Field, SQLType]]:
        """
        We override this to add in derived fields from the preliminary list created in the pre_derived field list.

        Right now, the only derived fields are:

        1. The relative keys built from every absolute key field specified in absolute_key_fields using the
        staticmethod get_relative_from_absolute.

        2. The measure counts built from every measure range field specified in measure_range_fields using the
        staticmethod get_measure_count_from_measure_range

        :return: a list of tuple pairs of fields with their sql type in the ordinal order that we want them in the table
        """

        new_list = []
        for field, sql_type in cls.field_sql_type_list_pre_derived_fields():

            new_list.append((field, sql_type))

            # If any field is in the set of absolute key fields, add the relative key version of it right afterwards
            if field in cls.absolute_key_fields():
                if sql_type != SQLType.TEXT and sql_type != SQLType.JSONB:
                    raise Exception("Field \"{}\" in class {} was marked as an absolute key field, which means it "
                                    "should have a SQLType of TEXT OR JSONB instead of {}"
                                    "".format(field.name, cls.__name__, sql_type))
                relative_key_field = cls.get_relative_from_absolute(field)
                new_list.append((relative_key_field, sql_type))

            if field in cls.measure_range_fields():
                if sql_type != SQLType.TEXT and sql_type != SQLType.JSONB:
                    raise Exception("Field \"{}\" in class {} was marked as a measure range, which means it "
                                    "should have a SQLType of TEXT OR JSONB instead of {}"
                                    "".format(field.name, cls.__name__, sql_type))
                measure_count_field = cls.get_measure_count_from_measure_range(field)
                new_list.append((measure_count_field, sql_type))

        return new_list


class Introduction(SonataBlockTableSpecification):
    """
    The table representing items particular to the introduction block in a sonata.
    """

    @classmethod
    def schema_table(cls) -> SchemaTable:
        return SchemaTable(sonata_archives_schema, "sonata_introduction")

    NUM_CYCLES = Field("num_cycles", "Introduction Number of Cycles")
    MEASURES = Field("measures", "Introduction Measures")
    INTRODUCTION_TYPE = Field("introduction_type", "Introduction Type")
    OPENING_KEY = Field("opening_key", "Introduction Opening Key")
    OPENING_TEMPO = Field("opening_tempo", "Introduction Opening Tempo")

    INTRODUCTION_OTHER_KEYS = Field("introduction_other_keys", "Introduction Other Key(s)")
    P_THEME_FORESHADOWED = Field("p_theme_recalled", "P Theme Recalled")
    TR_THEME_FORESHADOWED = Field("tr_theme_foreshadowed", "TR Theme Foreshadowed")
    S_THEME_FORESHADOWED = Field("s_theme_foreshadowed", "S Theme Foreshadowed")
    C_THEME_FORESHADOWED = Field("c_theme_foreshadowed", "C Theme Foreshadowed")

    # I

    # whether the intro contains a novel theme
    INTRO_THEME_PRESENT = Field("intro_theme_present", "Introduction Novel Theme Present")
    INTRO_THEME_KEY = Field("intro_theme_key", "Introduction Novel Theme Key")
    INTRO_THEME_DESCRIPTION = Field("intro_theme_description", "Introduction Theme Description")

    ENDING_KEY = Field("ending_key", "Introduction Ending Key")
    ENDING_CADENCE = Field("ending_cadence", "Introduction Ending Cadence")

    @classmethod
    def absolute_key_fields(cls) -> Set[Field]:
        return {
            cls.OPENING_KEY,
            cls.INTRO_THEME_KEY,
            cls.INTRODUCTION_OTHER_KEYS,
            cls.ENDING_KEY,
        }

    @classmethod
    def measure_range_fields(cls) -> Set[Field]:
        return {
            cls.MEASURES,
        }

    @classmethod
    def field_sql_type_list_pre_derived_fields(cls) -> List[Tuple[Field, SQLType]]:
        return [
            (cls.ID, SQLType.TEXT),
            (cls.NUM_CYCLES, SQLType.INTEGER),
            (cls.MEASURES, SQLType.TEXT),
            (cls.INTRODUCTION_TYPE, SQLType.TEXT),
            (cls.OPENING_TEMPO, SQLType.TEXT),
            (cls.OPENING_KEY, SQLType.TEXT),

            (cls.INTRODUCTION_OTHER_KEYS, SQLType.JSONB),  # JSONArray
            (cls.P_THEME_FORESHADOWED, SQLType.BOOLEAN),
            (cls.TR_THEME_FORESHADOWED, SQLType.BOOLEAN),
            (cls.S_THEME_FORESHADOWED, SQLType.BOOLEAN),
            (cls.C_THEME_FORESHADOWED, SQLType.BOOLEAN),

            # I Theme
            (cls.INTRO_THEME_PRESENT, SQLType.BOOLEAN),
            (cls.INTRO_THEME_KEY, SQLType.TEXT),
            (cls.INTRO_THEME_DESCRIPTION, SQLType.TEXT),
            (cls.ENDING_KEY, SQLType.TEXT),
            (cls.ENDING_CADENCE, SQLType.TEXT),
        ]

    @classmethod
    def create_constraints_sql(cls) -> sql.Composable:
        return sql.SQL("ALTER TABLE {st} ADD PRIMARY KEY ({id});").format(st=cls.schema_table(), id=cls.ID)


class Exposition(SonataBlockTableSpecification):
    """
    The table representing items particular to the exposition block in a sonata.
    """

    @classmethod
    def schema_table(cls) -> SchemaTable:
        return SchemaTable(sonata_archives_schema, "sonata_exposition")

    # Recap will override the display names on all of these
    NUM_CYCLES = Field("num_cycles", "Exposition Number of Cycles")  # does not include literal exposition repeats
    MEASURES = Field("measures", "Exposition Measures")
    OPENING_TEMPO = Field("opening_tempo", "Exposition Opening Tempo")

    # P
    P_THEME_MEASURES = Field("p_theme_measures", "P Theme Measures")
    P_THEME_OPENING_KEY = Field("p_theme_opening_key", "P Theme Opening Key")
    P_THEME_DESCRIPTION = Field("p_theme_description", "P Theme Description")
    P_THEME_PHRASE_STRUCTURE = Field("p_theme_phrase_structure", "P Theme Phrase Structure")
    P_THEME_OTHER_KEYS = Field("p_theme_other_keys", "P Theme Other Key(s)")
    P_THEME_ENDING_KEY = Field("p_theme_ending_key", "P Theme Ending Key")
    P_THEME_ENDING_CADENCE = Field("p_theme_ending_cadence", "P Theme Ending Cadence")

    # TR
    TR_THEME_PRESENT = Field("tr_theme_present", "TR Theme Present")
    TR_THEME_MEASURES = Field("tr_theme_measures", "TR Theme Measures")
    TR_THEME_OPENING_KEY = Field("tr_theme_opening_key", "TR Theme Opening Key")
    TR_THEME_DESCRIPTION = Field("tr_theme_description", "TR Theme Description")
    TR_THEME_P_BASED = Field("tr_theme_p_based", "TR Theme P-Based")
    TR_THEME_PHRASE_STRUCTURE = Field("tr_theme_phrase_structure", "TR Theme Phrase Structure")
    TR_THEME_OTHER_KEYS = Field("tr_theme_other_keys", "TR Theme Other Key(s)")
    TR_THEME_CHROMATIC_PREDOMINANT = Field("tr_theme_chromatic_predominant", "TR Theme Chromatic Predominant")
    TR_THEME_DOMINANT_LOCK = Field("tr_theme_dominant_lock", "TR Theme Dominant Lock")
    TR_THEME_ENERGY = Field("tr_theme_energy", "TR Theme Energy")
    TR_THEME_HAMMER_BLOW_COUNT = Field("tr_final_hammer_blow_count", "TR Theme Final Hammer Blows")
    TR_THEME_ENDING_KEY = Field("tr_theme_ending_key", "TR Theme Ending Key")
    TR_THEME_ENDING_CADENCE = Field("tr_theme_ending_cadence", "TR Theme Ending Cadence")

    # MC
    MC_PRESENT = Field("mc_present", "MC Present")
    MC_MEASURES = Field("mc_measures", "MC Measure(s)")
    MC_TYPE = Field("mc_type", "MC Type")

    # S
    S_THEME_PRESENT = Field("s_theme_present", "S Theme Present")
    S_THEME_MEASURES = Field("s_theme_measures", "S Theme Measures")
    S_THEME_OPENING_KEY = Field("s_theme_opening_key", "S Theme Opening Key")
    S_THEME_DESCRIPTION = Field("s_theme_description", "S Theme Description")
    S_THEME_P_BASED = Field("s_theme_p_based", "S Theme P-Based")
    S_THEME_PHRASE_STRUCTURE = Field("s_theme_phrase_structure", "S Theme Phrase Structure")
    S_THEME_OTHER_KEYS = Field("s_theme_other_keys", "S Theme Other Key(s)")
    S_THEME_ENDING_KEY = Field("s_theme_ending_key", "S Theme Ending Key")
    S_THEME_ENDING_CADENCE = Field("s_theme_ending_cadence", "S Theme Ending Cadence")

    # EEC
    # Note: naming raw name with both EEC and ESC so Recap can truly inherit all fields from Exposition
    # Only its display name will be different for Recap
    EEC_ESC_PRESENT = Field("eec_esc_present", "EEC Present")
    EEC_ESC_FAKE_OUT_COUNT = Field("eec_esc_fake_out_count", "EEC Fake Outs")
    EEC_ESC_STRENGTH = Field("eec_esc_strength", "EEC Strength")

    # C
    C_THEME_PRESENT = Field("c_theme_present", "C Theme Present")
    C_THEME_MEASURES = Field("c_theme_measures", "C Theme Measures")
    C_THEME_OPENING_KEY = Field("c_theme_opening_key", "C Theme Opening Key")
    C_THEME_DESCRIPTION = Field("c_theme_description", "C Theme Description")
    C_THEME_P_BASED = Field("c_theme_p_based", "C Theme P-Based")
    C_THEME_OTHER_KEYS = Field("c_theme_other_keys", "C Theme Other Key(s)")
    C_THEME_PHRASE_STRUCTURE = Field("c_theme_phrase_structure", "C Theme Phrase Structure")
    C_THEME_ENDING_KEY = Field("c_theme_ending_key", "C Theme Ending Key")
    C_THEME_ENDING_CADENCE = Field("c_theme_ending_cadence", "C Theme Ending Cadence")

    @classmethod
    def absolute_key_fields(cls) -> Set[Field]:
        return {
            cls.P_THEME_OPENING_KEY,
            cls.P_THEME_OTHER_KEYS,
            cls.P_THEME_ENDING_KEY,
            cls.TR_THEME_OPENING_KEY,
            cls.TR_THEME_OTHER_KEYS,
            cls.TR_THEME_ENDING_KEY,
            cls.S_THEME_OPENING_KEY,
            cls.S_THEME_OTHER_KEYS,
            cls.S_THEME_ENDING_KEY,
            cls.C_THEME_OPENING_KEY,
            cls.C_THEME_OTHER_KEYS,
            cls.C_THEME_ENDING_KEY
        }
    
    @classmethod
    def measure_range_fields(cls) -> Set[Field]:
        return {
            cls.MEASURES,
            cls.P_THEME_MEASURES,
            cls.TR_THEME_MEASURES,
            cls.MC_MEASURES,
            cls.S_THEME_MEASURES,
            cls.C_THEME_MEASURES,
        }

    # Helper methods so the recap can easily insert new attributes after or before phases of the exposition
    @classmethod
    def _general_field_sql_type_list(cls) -> List[Tuple[Field, SQLType]]:
        return [
            (cls.ID, SQLType.TEXT),
            (cls.NUM_CYCLES, SQLType.INTEGER),
            (cls.MEASURES, SQLType.TEXT),
            (cls.OPENING_TEMPO, SQLType.TEXT),
        ]

    @classmethod
    def _p_field_sql_type_list(cls) -> List[Tuple[Field, SQLType]]:
        return [
            (cls.P_THEME_MEASURES, SQLType.TEXT),
            (cls.P_THEME_OPENING_KEY, SQLType.TEXT),
            (cls.P_THEME_DESCRIPTION, SQLType.TEXT),
            (cls.P_THEME_PHRASE_STRUCTURE, SQLType.JSONB),
            (cls.P_THEME_OTHER_KEYS, SQLType.JSONB),  # JSONArray
            (cls.P_THEME_ENDING_KEY, SQLType.TEXT),
            (cls.P_THEME_ENDING_CADENCE, SQLType.TEXT),
        ]

    @classmethod
    def _tr_field_sql_type_list(cls) -> List[Tuple[Field, SQLType]]:
        return [
            (cls.TR_THEME_PRESENT, SQLType.BOOLEAN_DEFAULT_TRUE),
            (cls.TR_THEME_MEASURES, SQLType.TEXT),
            (cls.TR_THEME_OPENING_KEY, SQLType.TEXT),
            (cls.TR_THEME_P_BASED, SQLType.BOOLEAN),
            (cls.TR_THEME_DESCRIPTION, SQLType.TEXT),
            (cls.TR_THEME_PHRASE_STRUCTURE, SQLType.JSONB),
            (cls.TR_THEME_OTHER_KEYS, SQLType.TEXT),  # JSONArray
            (cls.TR_THEME_CHROMATIC_PREDOMINANT, SQLType.BOOLEAN),
            (cls.TR_THEME_DOMINANT_LOCK, SQLType.BOOLEAN),
            (cls.TR_THEME_ENERGY, SQLType.TEXT),
            (cls.TR_THEME_HAMMER_BLOW_COUNT, SQLType.INTEGER),
            (cls.TR_THEME_ENDING_KEY, SQLType.TEXT),
            (cls.TR_THEME_ENDING_CADENCE, SQLType.TEXT),

        ]

    @classmethod
    def _mc_field_sql_type_list(cls) -> List[Tuple[Field, SQLType]]:
        return [
            (cls.MC_PRESENT, SQLType.BOOLEAN_DEFAULT_TRUE),
            (cls.MC_MEASURES, SQLType.TEXT),
            (cls.MC_TYPE, SQLType.TEXT),
        ]

    @classmethod
    def _s_field_sql_type_list(cls) -> List[Tuple[Field, SQLType]]:
        return [
            (cls.S_THEME_PRESENT, SQLType.BOOLEAN_DEFAULT_TRUE),
            (cls.S_THEME_MEASURES, SQLType.TEXT),
            (cls.S_THEME_OPENING_KEY, SQLType.TEXT),
            (cls.S_THEME_DESCRIPTION, SQLType.TEXT),
            (cls.S_THEME_P_BASED, SQLType.TEXT),
            (cls.S_THEME_PHRASE_STRUCTURE, SQLType.JSONB),
            (cls.S_THEME_OTHER_KEYS, SQLType.JSONB),  # JSONArray
            (cls.S_THEME_ENDING_KEY, SQLType.TEXT),
            (cls.S_THEME_ENDING_CADENCE, SQLType.TEXT),
            (cls.EEC_ESC_PRESENT, SQLType.BOOLEAN_DEFAULT_TRUE),
            (cls.EEC_ESC_FAKE_OUT_COUNT, SQLType.INTEGER),
            (cls.EEC_ESC_STRENGTH, SQLType.TEXT),
        ]

    @classmethod
    def _c_field_sql_type_list(cls) -> List[Tuple[Field, SQLType]]:
        return [
            (cls.C_THEME_PRESENT, SQLType.BOOLEAN_DEFAULT_TRUE),
            (cls.C_THEME_OPENING_KEY, SQLType.TEXT),
            (cls.C_THEME_MEASURES, SQLType.TEXT),
            (cls.C_THEME_DESCRIPTION, SQLType.TEXT),
            (cls.C_THEME_P_BASED, SQLType.BOOLEAN),
            (cls.C_THEME_PHRASE_STRUCTURE, SQLType.JSONB),
            (cls.C_THEME_OTHER_KEYS, SQLType.JSONB),  # JSONArray
            (cls.C_THEME_ENDING_KEY, SQLType.TEXT),
            (cls.C_THEME_ENDING_CADENCE, SQLType.TEXT),
        ]

    # Builds this from all the private methods
    @classmethod
    def field_sql_type_list_pre_derived_fields(cls) -> List[Tuple[Field, SQLType]]:
        list_of_lists = [
            cls._general_field_sql_type_list(),
            cls._p_field_sql_type_list(),
            cls._tr_field_sql_type_list(),
            cls._mc_field_sql_type_list(),
            cls._s_field_sql_type_list(),
            cls._c_field_sql_type_list()
        ]
        # Flatten list of lists
        return [item for sublist in list_of_lists for item in sublist]

    @classmethod
    def create_constraints_sql(cls) -> sql.Composable:
        return sql.SQL("ALTER TABLE {st} ADD PRIMARY KEY ({id});").format(st=cls.schema_table(), id=cls.ID)


class Development(SonataBlockTableSpecification):
    """
    The table representing items particular to the coda block in a sonata.
    """

    @classmethod
    def schema_table(cls) -> SchemaTable:
        return SchemaTable(sonata_archives_schema, "sonata_development")

    NUM_CYCLES = Field("num_cycles", "Development Number of Cycles")
    MEASURES = Field("measures", "Development Measures")
    DEVELOPMENT_TYPE = Field("development_type", "Development Type")
    OPENING_TEMPO = Field("opening_tempo", "Opening Tempo")
    OPENING_KEY = Field("opening_key", "Development Opening Key")
    DEVELOPMENT_OTHER_KEYS = Field("development_other_keys", "Development Other Key(s)")
    # JSONArray of all keys IN ORDER between opening key and ending key

    # Episodes
    NUM_EPISODES = Field("num_episodes", "Development Episodes")
    EPISODE_MEASURES = Field("episode_measures", "Episode Measures")  # a map of episode to a measure range
    EPISODE_DESCRIPTIONS = Field("episode_descriptions", "Episode Descriptions")
    EPISODE_TONAL_MAP = Field("episode_tonal_map", "Episode Tonal Map")  # a map of episode to the keys used
    EPISODE_THEME_MAP = Field("episode_theme_map",
                              "Episode Theme Map")  # a map of episode to the themes used P / S / TR / C

    P_THEME_INITIATED = Field("p_theme_initiated", "P Theme Initiated")
    P_THEME_DEVELOPED = Field("p_theme_developed", "P Theme Developed")
    TR_THEME_DEVELOPED = Field("tr_theme_developed", "TR Theme Developed")
    S_THEME_DEVELOPED = Field("s_theme_developed", "S Theme Developed")
    C_THEME_DEVELOPED = Field("c_theme_developed", "C Theme Developed")

    # Development Theme
    DEVELOPMENT_THEME_PRESENT = Field("development_theme_present", "Development Novel Theme Present")
    DEVELOPMENT_THEME_KEY = Field("development_theme_key", "Development Novel Theme Key")
    DEVELOPMENT_THEME_DESCRIPTION = Field("Development Theme Description")

    # Retransition
    RETRANSITION_PRESENT = Field("retransition_present", "Retransition Present")
    DEVELOPMENT_ENDING_KEY = Field("development_ending_key", "Development Ending Key")
    DEVELOPMENT_ENDING_CADENCE = Field("development_ending_cadence", "Development Ending Cadence")

    @classmethod
    def absolute_key_fields(cls) -> Set[Field]:
        return {
            cls.OPENING_KEY,
            cls.DEVELOPMENT_OTHER_KEYS,
            cls.DEVELOPMENT_THEME_KEY,
            cls.DEVELOPMENT_ENDING_KEY,
        }
    
    @classmethod
    def measure_range_fields(cls) -> Set[Field]:
        return {
            cls.MEASURES,
            cls.EPISODE_MEASURES,
        }

    @classmethod
    def field_sql_type_list_pre_derived_fields(cls) -> List[Tuple[Field, SQLType]]:
        return [
            (cls.ID, SQLType.TEXT),
            (cls.NUM_CYCLES, SQLType.INTEGER),
            (cls.MEASURES, SQLType.TEXT),
            (cls.DEVELOPMENT_TYPE, SQLType.TEXT),
            (cls.OPENING_TEMPO, SQLType.TEXT),
            (cls.OPENING_KEY, SQLType.TEXT),

            (cls.DEVELOPMENT_OTHER_KEYS, SQLType.JSONB),  # JSONArray

            # Episodes
            (cls.NUM_EPISODES, SQLType.INTEGER),
            (cls.EPISODE_MEASURES, SQLType.JSONB),
            (cls.EPISODE_DESCRIPTIONS, SQLType.JSONB),
            (cls.EPISODE_THEME_MAP, SQLType.JSONB),
            (cls.EPISODE_TONAL_MAP, SQLType.JSONB),

            (cls.P_THEME_INITIATED, SQLType.BOOLEAN),
            (cls.P_THEME_DEVELOPED, SQLType.BOOLEAN),
            (cls.TR_THEME_DEVELOPED, SQLType.BOOLEAN),
            (cls.S_THEME_DEVELOPED, SQLType.BOOLEAN),
            (cls.C_THEME_DEVELOPED, SQLType.BOOLEAN),

            # Development Theme
            (cls.DEVELOPMENT_THEME_PRESENT, SQLType.BOOLEAN),
            (cls.DEVELOPMENT_THEME_KEY, SQLType.TEXT),
            (cls.DEVELOPMENT_THEME_DESCRIPTION, SQLType.TEXT),

            (cls.RETRANSITION_PRESENT, SQLType.BOOLEAN_DEFAULT_TRUE),
            (cls.DEVELOPMENT_ENDING_KEY, SQLType.TEXT),
            (cls.DEVELOPMENT_ENDING_CADENCE, SQLType.TEXT),
        ]

    @classmethod
    def create_constraints_sql(cls) -> sql.Composable:
        return sql.SQL("ALTER TABLE {st} ADD PRIMARY KEY ({id});").format(st=cls.schema_table(), id=cls.ID)


class Recapitulation(Exposition):
    """
    The table representing items particular to the recapitulation block in a sonata.

    Inherits from the Exposition since in general everything in the Exposition we want in the recap
    """

    @classmethod
    def schema_table(cls) -> SchemaTable:
        return SchemaTable(sonata_archives_schema, "sonata_recapitulation")

    # Override the display names on these exposition attributes
    NUM_CYCLES = Field("num_cycles", "Recapitulation Number of Cycles")  # does not include literal exposition repeats
    MEASURES = Field("measures", "Recapitulation Measures")
    OPENING_TEMPO = Field("opening_tempo", "Recapitulation Opening Tempo")

    # P
    P_THEME_PRESENT = Field("p_theme_present", "P Theme Present")  # Type 2 Sonatas don't recap P
    P_THEME_CHANGE_FROM_EXPOSITION = Field("p_theme_change_from_exposition", "P Theme Change From Exposition")

    # TR
    TR_THEME_CHANGE_FROM_EXPOSITION = Field("tr_theme_change_from_exposition", "TR Theme Change From Exposition")

    # S
    S_THEME_CHANGE_FROM_EXPOSITION = Field("s_theme_change_from_exposition", "S Theme Change From Exposition")

    # ESC

    # Override the display name since EEC vs ESC only core sonata thing named differently between the two halfs
    EEC_ESC_PRESENT = Field("eec_esc_present", "ESC Present")
    EEC_ESC_FAKE_OUT_COUNT = Field("eec_esc_fake_out_count", "ESC Fake Outs")
    EEC_ESC_STRENGTH = Field("eec_esc_strength", "ESC Strength")

    # C
    C_THEME_CHANGE_FROM_EXPOSITION = Field("c_theme_change_from_exposition", "C Theme Change From Exposition")

    # Builds this by using Exposition parent's lists with ability to add additional below each one
    # (This enables the new Recap elements to not have to be all at the end
    @classmethod
    def field_sql_type_list_pre_derived_fields(cls) -> List[Tuple[Field, SQLType]]:
        list_of_lists = [
            cls._general_field_sql_type_list(),
            [
                (cls.P_THEME_PRESENT, SQLType.BOOLEAN_DEFAULT_TRUE)
            ],
            cls._p_field_sql_type_list(),
            [
                (cls.P_THEME_CHANGE_FROM_EXPOSITION, SQLType.TEXT),
            ],

            cls._tr_field_sql_type_list(),
            [
                (cls.TR_THEME_CHANGE_FROM_EXPOSITION, SQLType.TEXT),
            ],

            cls._mc_field_sql_type_list(),
            [

            ],

            cls._s_field_sql_type_list(),
            [
                (cls.S_THEME_CHANGE_FROM_EXPOSITION, SQLType.TEXT),
            ],

            cls._c_field_sql_type_list(),
            [
                (cls.C_THEME_CHANGE_FROM_EXPOSITION, SQLType.TEXT),
            ],
        ]
        # Flatten list of lists
        return [item for sublist in list_of_lists for item in sublist]

    @classmethod
    def create_constraints_sql(cls) -> sql.Composable:
        return sql.SQL("ALTER TABLE {st} ADD PRIMARY KEY ({id});").format(st=cls.schema_table(), id=cls.ID)


class Coda(SonataBlockTableSpecification):
    """
    The table representing items particular to the coda block in a sonata.
    """

    @classmethod
    def schema_table(cls) -> SchemaTable:
        return SchemaTable(sonata_archives_schema, "sonata_coda")

    NUM_CYCLES = Field("num_cycles", "Coda Number of Cycles")
    MEASURES = Field("measures", "Coda Measures")
    CODA_TYPE = Field("coda_type", "Coda Type")
    OPENING_TEMPO = Field("opening_tempo", "Coda Opening Tempo")
    OPENING_KEY = Field("opening_key", "Coda Opening Key")

    CODA_OTHER_KEYS = Field("coda_other_keys", "Coda Other Key(s)")  # a JSONArray of keys tonicized
    P_THEME_RECALLED = Field("p_theme_recalled", "P Theme Recalled")
    TR_THEME_RECALLED = Field("tr_theme_recalled", "TR Theme Recalled")
    S_THEME_RECALLED = Field("s_theme_recalled", "S Theme Recalled")
    C_THEME_RECALLED = Field("c_theme_recalled", "C Theme Recalled")

    # Coda Theme
    CODA_THEME_PRESENT = Field("coda_theme_present", "Coda Novel Theme Present")
    CODA_THEME_KEY = Field("coda_theme_key", "Coda Novel Theme Key")
    CODA_THEME_DESCRIPTION = Field("coda_theme_description", "Coda Novel Theme Description")

    ENDING_KEY = Field("ending_key", "Coda Ending Key")
    ENDING_CADENCE = Field("ending_cadence", "Coda Ending Cadence")

    @classmethod
    def absolute_key_fields(cls) -> Set[Field]:
        return {
            cls.OPENING_KEY,
            cls.CODA_THEME_KEY,
            cls.ENDING_KEY,
        }

    @classmethod
    def measure_range_fields(cls) -> Set[Field]:
        return {
            cls.MEASURES
        }

    @classmethod
    def field_sql_type_list_pre_derived_fields(cls) -> List[Tuple[Field, SQLType]]:
        return [
            (cls.ID, SQLType.TEXT),
            (cls.NUM_CYCLES, SQLType.INTEGER),
            (cls.MEASURES, SQLType.TEXT),
            (cls.CODA_TYPE, SQLType.TEXT),
            (cls.OPENING_TEMPO, SQLType.TEXT),
            (cls.OPENING_KEY, SQLType.TEXT),

            (cls.CODA_OTHER_KEYS, SQLType.JSONB),  # JSONArray
            (cls.P_THEME_RECALLED, SQLType.BOOLEAN),
            (cls.TR_THEME_RECALLED, SQLType.BOOLEAN),
            (cls.S_THEME_RECALLED, SQLType.BOOLEAN),
            (cls.C_THEME_RECALLED, SQLType.BOOLEAN),

            # Coda Theme
            (cls.CODA_THEME_PRESENT, SQLType.BOOLEAN),
            (cls.CODA_THEME_KEY, SQLType.TEXT),
            (cls.CODA_THEME_DESCRIPTION, SQLType.TEXT),

            (cls.ENDING_KEY, SQLType.TEXT),
            (cls.ENDING_CADENCE, SQLType.TEXT),
        ]

    @classmethod
    def create_constraints_sql(cls) -> sql.Composable:
        return sql.SQL("ALTER TABLE {st} ADD PRIMARY KEY ({id});").format(st=cls.schema_table(), id=cls.ID)
