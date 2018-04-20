#!/usr/bin/env python
"""
A module containing the specification for the base SQL tables (and views, which act like tables)
"""
from abc import abstractmethod
from typing import Tuple, List, Set, Any, Dict, Union

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
    def create_constraints_sql(cls) -> Union[sql.Composable, None]:
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
            (cls.ID, SQLType.TEXT_PRIMARY_KEY),
            (cls.FULL_NAME, SQLType.TEXT),
            (cls.SURNAME, SQLType.TEXT),
            (cls.NATIONALITY, SQLType.TEXT),
            (cls.BIRTH_DATE, SQLType.DATE),
            (cls.DEATH_DATE, SQLType.DATE),
            (cls.BIRTHPLACE, SQLType.TEXT),
            (cls.PRIMARY_RESIDENCE, SQLType.TEXT),
        ]

    @classmethod
    def create_constraints_sql(cls) -> Union[sql.Composable, None]:
        return None


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
            (cls.ID, SQLType.TEXT_PRIMARY_KEY),
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
    def create_constraints_sql(cls) -> Union[sql.Composable, None]:
        return sql.SQL("ALTER TABLE {st} ADD FOREIGN KEY ({comp_id}) REFERENCES {c_st}({c_id});") \
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
            (cls.ID, SQLType.TEXT_PRIMARY_KEY),
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
    def create_constraints_sql(cls) -> Union[sql.Composable, None]:
        # Add ON DELETE CASCADE to the FK for the blocks so that if we delete a block it deletes the sonata
        # We are going to upsert the sonata at the end of adding all the blocks anyway, so this is just easier
        # to ensure that you clear its FK link to any block that has been deleted
        return sql.SQL("ALTER TABLE {st} ADD FOREIGN KEY ({piece_id}) REFERENCES {p_st}({p_id});\n"
                       "ALTER TABLE {st} ADD FOREIGN KEY ({intro_id}) REFERENCES {i_st}({i_id}) ON DELETE CASCADE;\n"
                       "ALTER TABLE {st} ADD FOREIGN KEY ({expo_id}) REFERENCES {e_st}({e_id}) ON DELETE CASCADE;\n"
                       "ALTER TABLE {st} ADD FOREIGN KEY ({devel_id}) REFERENCES {d_st}({d_id}) ON DELETE CASCADE;\n"
                       "ALTER TABLE {st} ADD FOREIGN KEY ({recap_id}) REFERENCES {r_st}({r_id}) ON DELETE CASCADE;\n"
                       "ALTER TABLE {st} ADD FOREIGN KEY ({coda_id}) REFERENCES {c_st}({c_id}) ON DELETE CASCADE;"
                       ).format(st=cls.schema_table(), id=cls.ID,
                                piece_id=cls.PIECE_ID, p_st=Piece.schema_table(), p_id=Piece.ID,
                                intro_id=cls.INTRODUCTION_ID, i_st=Intro.schema_table(), i_id=Piece.ID,
                                expo_id=cls.EXPOSITION_ID, e_st=Expo.schema_table(), e_id=Piece.ID,
                                devel_id=cls.DEVELOPMENT_ID, d_st=Development.schema_table(), d_id=Piece.ID,
                                recap_id=cls.RECAPITULATION_ID, r_st=Recap.schema_table(), r_id=Piece.ID,
                                coda_id=cls.CODA_ID, c_st=Coda.schema_table(), c_id=Piece.ID)


class SonataBlockTableSpecification(TableSpecification):
    """
    An ABC Table Specification for a sonata block that contains some additional functionality that will be shared
    across each of the sonata blocks
    """

    # All blocks must have the same ID column and piece ID
    ID = Field("id")
    SONATA_ID = Field("sonata_id")

    """
    SUPPORT FOR DERIVED FIELDS
    """

    @classmethod
    @abstractmethod
    def absolute_key_fields(cls) -> Set[Field]:
        """
        Returns a set of all absolute key fields, which will be the set of fields for which we will derive a
        corresponding relative key field.

        :return: a set of fields corresponding to all the fields that are for absolute keys
        """

    @staticmethod
    def get_relative_key_field_from_absolute_key_field(absolute_key_field: Field) -> Field:
        """
        Given a field name with the word 'key' implying absolute, dynamically replaces it with 'relative key'.
        Replaces the display name "Key" with "Relative Key".

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
    def measure_range_fields_to_compute_measure_counts(cls) -> Set[Field]:
        """
        Returns a set of all measure range fields, which will be the set of fields for which we will add a
        corresponding measure count derived field.

        :return: a set of fields corresponding to all the fields that are for measure ranges that are not going
        to be single measures and is thus worth deriving counts for.
        """

    @staticmethod
    def get_measure_count_field_from_measure_range_field(measure_range_field: Field) -> Field:
        """
        Given a field name with the word 'measure', dynamically replaces it with 'measure count'

        :param measure_range_field: the name of the measure range. Must contain the word "measures"
        :return: a new Field with 'measures' switched out for 'measure count' as its name
        """
        name = measure_range_field.name
        display_name = measure_range_field.display_name

        if 'measures' not in name or 'Measures' not in display_name:
            raise Exception("Field {} with display_name {} marked as a MeasureRange but didn't contain \"measures\" "
                            "in its name or \"Measures\" in its display name!".format(name, display_name))
        else:
            return Field(name.replace('measures', 'measure_count'),
                         display_name=display_name.replace('Measures', 'Measure Count'))

    @classmethod
    @abstractmethod
    def measures_array_fields_to_compute_counts(cls) -> Set[Field]:
        """
        Returns a set of all measure array fields, which will be the set of fields for which we will add a
        corresponding count of the number of measure elements in an array. Note: this is not for deriving counts of
        measures in each range (it should be 1 for each range), we will basically simply derive the length of the
        JSONArray.

        :return: a set of JSONArray fields of single-measure elements that we want to derive the counts of (i.e.
        the number of measure elements of the JSONArray)
        """

    @staticmethod
    def get_count_field_from_measures_array_field(measures_array_field: Field) -> Field:
        """
        Given a JSONArray field wit the word 'measures', dynamically replaces it with count.

        :param measures_array_field: a JSONArray field of measures that we wish to count
        :return: a new Field with 'measures' switched out for 'count' as its name
        """
        name = measures_array_field.name
        display_name = measures_array_field.display_name

        if 'measures' not in name or 'Measure(s)' not in display_name:
            raise Exception("Field {} with display_name {} marked as a MeasureRange but didn't contain \"measures\" "
                            "in its name or \"Measure(s)\" in its display name!".format(name, display_name))
        else:
            return Field(name.replace('measures', 'count'),
                         display_name=display_name.replace('Measure(s)', 'Count'))

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
        staticmethod get_relative_key_field_from_absolute_key_field.

        2. The measure counts built from every measure range field specified in
        measure_range_fields_to_compute_measure_counts using the staticmethod
        get_measure_count_field_from_measure_range_field

        3. The count of measures built from all single measures specified in measure array field field in
        measures_array_fields_to_compute_counts using the staticmethod get_count_field_from_measures_array_field

        elements in a JSONArray of measures, using

        :return: a list of tuple pairs of fields with their sql type in the ordinal order that we want them in the table
        """

        new_list = []
        for field, sql_type in cls.field_sql_type_list_pre_derived_fields():

            # If necessary, compute the count of measure elements in the JSON Array right before it:
            if field in cls.measures_array_fields_to_compute_counts():
                if sql_type != SQLType.JSONB and sql_type != SQLType.JSONB_DEFAULT_EMPTY_ARRAY:
                    raise Exception("Field \"{}\" in class {} was marked as a measure array field, which means it"
                                    "should have a SQLType of JSONB instead of {}"
                                    "".format(field.name, cls.__name__, sql_type))
                count_field = cls.get_count_field_from_measures_array_field(field)
                new_list.append((count_field, SQLType.INTEGER_DEFAULT_ZERO))

            new_list.append((field, sql_type))

            # If necessary, add the relative key version of it right afterwards
            if field in cls.absolute_key_fields():
                if sql_type != SQLType.TEXT and sql_type != SQLType.JSONB:
                    raise Exception("Field \"{}\" in class {} was marked as an absolute key field, which means it "
                                    "should have a SQLType of TEXT OR JSONB instead of {}"
                                    "".format(field.name, cls.__name__, sql_type))
                relative_key_field = cls.get_relative_key_field_from_absolute_key_field(field)
                new_list.append((relative_key_field, sql_type))

            # If necessary, compute the measure length right after it
            if field in cls.measure_range_fields_to_compute_measure_counts():
                if sql_type != SQLType.TEXT and sql_type != SQLType.JSONB:
                    raise Exception("Field \"{}\" in class {} was marked as a measure range, which means it "
                                    "should have a SQLType of TEXT OR JSONB instead of {}"
                                    "".format(field.name, cls.__name__, sql_type))
                measure_count_field = cls.get_measure_count_field_from_measure_range_field(field)
                new_list.append((measure_count_field, sql_type))

        return new_list

    @classmethod
    def create_constraints_sql(cls) -> Union[sql.Composable, None]:
        return sql.SQL("ALTER TABLE {st} ADD FOREIGN KEY ({sonata_id}) REFERENCES {s_st}({s_id}) ON DELETE CASCADE;"
                       ).format(st=cls.schema_table(), id=cls.ID, sonata_id=cls.SONATA_ID,
                                s_st=Sonata.schema_table(), s_id=Sonata.ID)


class Intro(SonataBlockTableSpecification):
    """
    The table representing items particular to the introduction block in a sonata.
    """

    @classmethod
    def schema_table(cls) -> SchemaTable:
        return SchemaTable(sonata_archives_schema, "sonata_introduction")

    NUM_CYCLES = Field("num_cycles", "Introduction Number of Cycles")
    MEASURES = Field("measures", "Introduction Measures")
    INTRODUCTION_TYPE = Field("introduction_type", "Introduction Type")
    COMMENTS = Field("comments", "Introduction Comments")
    OPENING_KEY = Field("opening_key", "Introduction Opening Key")
    OPENING_TEMPO = Field("opening_tempo", "Introduction Opening Tempo")

    OTHER_KEYS_LIST = Field("other_keys", "Introduction Other Key(s)")

    EXPOSITION_WINDUP = Field("expoistion_windup", "Exposition Wind-up")
    EXPOSITION_WINDUP_MEASURE = Field("exposition_windup_measure", "Exposition Wind-up Start Measure")
    ENDING_KEY = Field("ending_key", "Introduction Ending Key")
    ENDING_CADENCE = Field("ending_cadence", "Introduction Ending Cadence")

    @classmethod
    def absolute_key_fields(cls) -> Set[Field]:
        return {
            cls.OPENING_KEY,
            cls.OTHER_KEYS_LIST,
            cls.ENDING_KEY,
        }

    @classmethod
    def measure_range_fields_to_compute_measure_counts(cls) -> Set[Field]:
        return {
            cls.MEASURES,
        }

    @classmethod
    def measures_array_fields_to_compute_counts(cls) -> Set[Field]:
        return set()

    @classmethod
    def field_sql_type_list_pre_derived_fields(cls) -> List[Tuple[Field, SQLType]]:
        return [
            (cls.ID, SQLType.TEXT_PRIMARY_KEY),
            (cls.SONATA_ID, SQLType.TEXT),
            (cls.MEASURES, SQLType.TEXT),
            (cls.NUM_CYCLES, SQLType.INTEGER),
            (cls.INTRODUCTION_TYPE, SQLType.TEXT),
            (cls.COMMENTS, SQLType.TEXT),
            (cls.OPENING_TEMPO, SQLType.TEXT),
            (cls.OPENING_KEY, SQLType.TEXT),
            (cls.OTHER_KEYS_LIST, SQLType.JSONB),
            (cls.EXPOSITION_WINDUP, SQLType.BOOLEAN_DEFAULT_FALSE),
            (cls.EXPOSITION_WINDUP_MEASURE, SQLType.TEXT),
            (cls.ENDING_KEY, SQLType.TEXT),
            (cls.ENDING_CADENCE, SQLType.TEXT),
        ]


class Expo(SonataBlockTableSpecification):
    """
    The table representing items particular to the exposition block in a sonata.
    """

    @classmethod
    def schema_table(cls) -> SchemaTable:
        return SchemaTable(sonata_archives_schema, "sonata_exposition")

    # Recap will override the display names on all of these
    NUM_CYCLES = Field("num_cycles", "Exposition Number of Cycles")  # does not include literal exposition repeats
    MEASURES = Field("measures", "Exposition Measures")
    CONTINUOUS = Field("continuous", "Continuous Exposition")  # No TR, MC or S
    CONTINUOUS_SUBTYPE = Field("continuous_subtype", "Continuous Exposition Subtype")
    DUTCHMAN_TYPE = Field("dutchman_type", "Dutchman-Type Exposition")  # Maximally contrasting Masculine P, Feminine S
    COMMENTS = Field("comments", "Exposition Comments")
    OPENING_TEMPO = Field("opening_tempo", "Exposition Opening Tempo")

    # P
    P_MEASURES = Field("p_theme_measures", "P Theme Measures")
    P_COMMENTS = Field("p_theme_comments", "P Theme Description")
    P_TYPE = Field("p_theme_type", "P Theme Type")
    P_MODULE_MEASURES_DICT = Field("p_module_measures", "P Module Measures")
    # Rarely used since multimodule Ps have descriptive single type that rarely need types for each module
    P_MODULE_TYPES_DICT = Field("p_module_types", "P Module Types")
    P_MODULE_PHRASE_DICT = Field("p_module_phrase_structure", "P Module Phrase Structure")
    P_MODULE_DYNAMICS_DICT = Field("p_module_dynamics", "P Module Dynamics")
    P_PAC_MEASURES_LIST = Field("p_theme_pac_measures", "P Theme PAC Measure(s)")
    P_OPENING_KEY = Field("p_theme_opening_key", "P Theme Opening Key")
    P_OTHER_KEYS_LIST = Field("p_theme_other_keys", "P Theme Other Key(s)")
    P_ENDING_KEY = Field("p_theme_ending_key", "P Theme Ending Key")
    P_ENDING_CADENCE = Field("p_theme_ending_cadence", "P Theme Ending Cadence")

    # TR
    TR_PRESENT = Field("tr_theme_present", "TR Theme Present")
    TR_MEASURES = Field("tr_theme_measures", "TR Theme Measures")
    TR_COMMENTS = Field("tr_theme_comments", "TR Theme Comments")
    TR_TYPE = Field("tr_theme_type", "TR Theme Type")
    TR_MODULE_MEASURES_DICT = Field("tr_module_measures", "TR Module Measures")
    TR_MODULE_TYPES_DICT = Field("tr_module_types", "TR Module Types")  # Only use if Mixed Transition
    TR_MODULE_PHRASE_DICT = Field("tr_module_phrase_structure", "TR Module Phrase Structure")
    TR_MODULE_DYNAMICS_DICT = Field("tr_module_dynamics", "TR Module Dynamics")
    TR_CHROM_PREDOM = Field("tr_theme_chromatic_predominant", "TR Theme Chromatic Predominant")
    TR_DOMINANT_LOCK = Field("tr_theme_dominant_lock", "TR Theme Dominant Lock")
    TR_ENERGY = Field("tr_theme_energy", "TR Theme Energy")
    TR_HAMMER_COUNT = Field("tr_final_hammer_blow_count", "TR Theme Final Hammer Blows")
    # The measures of any quasi-MC Effects or Early PAC in Continuous Exposition Subtype 2:
    TR_MC_EFFECT_MEASURES_LIST = Field("tr_theme_mc_effect_measures", "TR Theme MC Effect Measure(s)")
    TR_PAC_MEASURES_LIST = Field("tr_theme_pac_measures", "TR Theme PAC Measure(s)")

    TR_OPENING_KEY = Field("tr_theme_opening_key", "TR Theme Opening Key")
    TR_OTHER_KEYS_LIST = Field("tr_theme_other_keys", "TR Theme Other Key(s)")
    TR_ENDING_KEY = Field("tr_theme_ending_key", "TR Theme Ending Key")  #
    TR_ENDING_CADENCE = Field("tr_theme_ending_cadence", "TR Theme Ending Cadence")

    # MC
    MC_PRESENT = Field("mc_present", "MC Present")
    MC_MEASURES = Field("mc_measures", "MC Measures")
    MC_DYNAMICS = Field("mc_dynamics", "MC Dynamics")
    _MC_TYPE = Field("mc_type", "MC Type")  # Derived field from TR Ending Relative Key and Ending Cadence
    MC_COMMENTS = Field("mc_comments", "MC Comments")
    MC_STYLE = Field("mc_style", "MC Style")  # Whether caesura fill, general pause, S0 affect etc.
    MC_FILL_KEY = Field("mc_fill_key", "MC Fill Key")  # Only fill out if different from TR Ending Key
    # This is usually only a parallel mode shift (i.e. TR implies C minor but MC implies C major)

    # S
    S_PRESENT = Field("s_theme_present", "S Theme Present")
    S_MEASURES = Field("s_theme_measures", "S Theme Measures")
    S_COMMENTS = Field("s_theme_comments", "S Theme Comments")
    S_TYPE = Field("s_theme_type", "S Theme Type")
    S_MODULE_MEASURES_DICT = Field("s_module_measures", "S Module Measures")
    S_MODULE_TYPES_DICT = Field("s_module_types", "S Module Types")
    S_MODULE_PHRASE_DICT = Field("s_module_phrase_structure", "S Module Phrase Structure")
    S_MODULE_DYNAMICS_DICT = Field("s_module_dynamics", "S Module Dynamics")
    # These will be a JSON Array of all cadence measures, since they are all 1 measure long, no need for counts
    S_STRONG_PAC_MEAS_LIST = Field("s_theme_strong_pac_measures", "S Theme Strong PAC Measure(s)")
    S_ATTEN_PAC_MEAS_LIST = Field("s_theme_attenuated_pac_measures", "S Theme Attenuated PAC Measure(s)")
    # Evaded PACs mean non-PACs that would have been PACs (dramatic root position active Vs)
    # but are either resolved imperfectly, deceptively, or with no resolution at all
    S_EVADED_PAC_MEAS_LIST = Field("s_theme_evaded_pac_measures", "S Theme Evaded PAC Measure(s)")
    S_OPENING_KEY = Field("s_theme_opening_key", "S Theme Opening Key")
    S_OTHER_KEYS_LIST = Field("s_theme_other_keys", "S Theme Other Key(s)")
    S_ENDING_KEY = Field("s_theme_ending_key", "S Theme Ending Key")
    S_ENDING_CADENCE = Field("s_theme_ending_cadence", "S Theme Ending Cadence")

    # EEC
    # Note: naming raw name with both EEC and ESC so Recap can truly inherit all fields from Exposition
    # Only its display name will be different for Recap
    EEC_ESC_SECURED = Field("eec_esc_secured", "EEC Secured")
    EEC_ESC_MEASURE = Field("eec_esc_measure", "EEC Measure")  # Always will be 1 measure long, so no need for counts
    EEC_ESC_COMMENTS = Field("eec_esc_comments", "EEC Comments")
    EEC_ESC_DYNAMICS = Field("eec_esc_dynamics", "EEC Dynamics")

    # C
    C_PRESENT = Field("c_theme_present", "C Theme Present")
    C_MEASURES_INCL_C_RT = Field("c_theme_measures", "C Theme Measures")  # Includes RT so it's the full zone
    C_COMMENTS = Field("c_theme_comments", "C Theme Comments")
    C_SC_PRE_EEC_ESC = Field("c_theme_sc_pre_eec_esc", "C Theme in S Space / Pre-EEC")
    C_TYPE = Field("c_theme_type", "C Theme Type")
    C_MODULE_MEASURES_DICT = Field("c_module_measures", "C Module Measures")
    C_MODULE_TYPES_DICT = Field("c_module_types", "C Module Types")
    C_MODULE_PHRASE_DICT = Field("c_module_phrase_structure", "C Module Phrase Structure")
    C_MODULE_DYNAMICS_DICT = Field("c_module_dynamics", "C Module Dynamics")
    C_PAC_MEASURES_LIST = Field("c_theme_pac_measures", "C Theme PAC Measure(s)")  # Always 1 measures
    C_OPENING_KEY = Field("c_theme_opening_key", "C Theme Opening Key")
    C_OTHER_KEYS_LIST = Field("c_theme_other_keys", "C Theme Other Key(s)")
    C_ENDING_KEY_BEFORE_C_RT = Field("c_theme_ending_key", "C Theme Ending Key")  # Before RT
    C_RT_PRESENT = Field("c_rt_present", "C-RT Present")
    C_RT_MEASURES = Field("c_rt_measures", "C-RT Measures")
    C_RT_ENDING_KEY = Field("c_rt_ending_key", "C-RT Ending Key")
    C_RT_DYNAMICS = Field("c_rt_dynamics", "C-RT Dynamics")

    @classmethod
    def absolute_key_fields(cls) -> Set[Field]:
        return {
            cls.P_OPENING_KEY,
            cls.P_OTHER_KEYS_LIST,
            cls.P_ENDING_KEY,
            cls.TR_OPENING_KEY,
            cls.TR_OTHER_KEYS_LIST,
            cls.TR_ENDING_KEY,
            cls.MC_FILL_KEY,
            cls.S_OPENING_KEY,
            cls.S_OTHER_KEYS_LIST,
            cls.S_ENDING_KEY,
            cls.C_OPENING_KEY,
            cls.C_OTHER_KEYS_LIST,
            cls.C_ENDING_KEY_BEFORE_C_RT,
            cls.C_RT_ENDING_KEY,
        }

    @classmethod
    def measure_range_fields_to_compute_measure_counts(cls) -> Set[Field]:
        return {
            cls.MEASURES,
            cls.P_MEASURES,
            cls.P_MODULE_MEASURES_DICT,
            cls.TR_MEASURES,
            cls.TR_MODULE_MEASURES_DICT,
            cls.MC_MEASURES,
            cls.S_MEASURES,
            cls.S_MODULE_MEASURES_DICT,
            cls.C_MEASURES_INCL_C_RT,
            cls.C_MODULE_MEASURES_DICT,
            cls.C_RT_MEASURES
        }

    @classmethod
    def measures_array_fields_to_compute_counts(cls) -> Set[Field]:
        return {
            cls.P_PAC_MEASURES_LIST,
            cls.TR_PAC_MEASURES_LIST,
            cls.TR_MC_EFFECT_MEASURES_LIST,
            cls.S_EVADED_PAC_MEAS_LIST,
            cls.S_STRONG_PAC_MEAS_LIST,
            cls.S_ATTEN_PAC_MEAS_LIST,
            cls.C_PAC_MEASURES_LIST,
        }

    @classmethod
    def fields_unlikely_to_be_same_for_exposition_and_recap(cls) -> Set[Field]:
        """
        This will get all fields that we don't want to automatically be copied from Exposition to Recap
        when getting recap_dict_from_exposition because they are extremely unlikely.

        These include all measure fields (both those for counts and not) and comment fields.

        Also included are many P-TR things (excluding keys) and all keys in S-C.

        :return: a set of fields
        """
        # Exclude all fields that involve comments or measures
        fields_to_exclude = set()
        fields_to_exclude.update(cls.measures_array_fields_to_compute_counts())
        fields_to_exclude.update(cls.measure_range_fields_to_compute_measure_counts())

        fields_to_exclude.update({
            # Measure fields not those already specified in
            cls.EEC_ESC_MEASURE,

            # Comments
            cls.COMMENTS,
            cls.P_COMMENTS,
            cls.TR_COMMENTS,
            cls.MC_COMMENTS,
            cls.S_COMMENTS,
            cls.EEC_ESC_COMMENTS,
            cls.C_COMMENTS,

            # Dynamics
            cls.P_MODULE_DYNAMICS_DICT,
            cls.TR_MODULE_DYNAMICS_DICT,
            cls.MC_DYNAMICS,
            cls.S_MODULE_DYNAMICS_DICT,
            cls.EEC_ESC_DYNAMICS,
            cls.C_MODULE_DYNAMICS_DICT,
            cls.C_RT_DYNAMICS,

            # Exposition Part 2 Keys that 99% of the time will be different in recap
            cls.TR_ENDING_KEY,
            cls.MC_FILL_KEY,
            cls.S_OPENING_KEY,
            cls.S_OTHER_KEYS_LIST,
            cls.S_ENDING_KEY,
            cls.C_OPENING_KEY,
            cls.C_OTHER_KEYS_LIST,
            cls.C_ENDING_KEY_BEFORE_C_RT,
            cls.C_RT_ENDING_KEY,
        })
        fields_to_exclude.update(cls.measures_array_fields_to_compute_counts())
        fields_to_exclude.update(cls.measure_range_fields_to_compute_measure_counts())
        return fields_to_exclude

    # Helper methods so the recap can easily insert new attributes after or before phases of the exposition
    @classmethod
    def _general_field_sql_type_list(cls) -> List[Tuple[Field, SQLType]]:
        return [
            (cls.ID, SQLType.TEXT_PRIMARY_KEY),
            (cls.SONATA_ID, SQLType.TEXT),
            (cls.MEASURES, SQLType.TEXT),
            (cls.NUM_CYCLES, SQLType.INTEGER),
            (cls.CONTINUOUS, SQLType.BOOLEAN_DEFAULT_FALSE),
            (cls.CONTINUOUS_SUBTYPE, SQLType.TEXT),
            (cls.DUTCHMAN_TYPE, SQLType.BOOLEAN_DEFAULT_FALSE),
            (cls.COMMENTS, SQLType.TEXT),
            (cls.OPENING_TEMPO, SQLType.TEXT),
        ]

    @classmethod
    def _p_field_sql_type_list(cls) -> List[Tuple[Field, SQLType]]:
        return [
            (cls.P_MEASURES, SQLType.TEXT),
            (cls.P_COMMENTS, SQLType.TEXT),
            (cls.P_TYPE, SQLType.TEXT),
            (cls.P_MODULE_MEASURES_DICT, SQLType.JSONB),
            (cls.P_MODULE_TYPES_DICT, SQLType.JSONB),
            (cls.P_MODULE_PHRASE_DICT, SQLType.JSONB),
            (cls.P_MODULE_DYNAMICS_DICT, SQLType.JSONB),
            (cls.P_PAC_MEASURES_LIST, SQLType.JSONB_DEFAULT_EMPTY_ARRAY),
            (cls.P_OPENING_KEY, SQLType.TEXT),
            (cls.P_OTHER_KEYS_LIST, SQLType.JSONB),
            (cls.P_ENDING_KEY, SQLType.TEXT),
            (cls.P_ENDING_CADENCE, SQLType.TEXT),
        ]

    @classmethod
    def _tr_field_sql_type_list(cls) -> List[Tuple[Field, SQLType]]:
        return [
            (cls.TR_PRESENT, SQLType.BOOLEAN_DEFAULT_TRUE),
            (cls.TR_MEASURES, SQLType.TEXT),
            (cls.TR_COMMENTS, SQLType.TEXT),
            (cls.TR_TYPE, SQLType.TEXT),
            (cls.TR_MODULE_MEASURES_DICT, SQLType.JSONB),
            (cls.TR_MODULE_TYPES_DICT, SQLType.JSONB),
            (cls.TR_MODULE_PHRASE_DICT, SQLType.JSONB),
            (cls.TR_MODULE_DYNAMICS_DICT, SQLType.JSONB),
            (cls.TR_CHROM_PREDOM, SQLType.BOOLEAN),
            (cls.TR_DOMINANT_LOCK, SQLType.BOOLEAN),
            (cls.TR_ENERGY, SQLType.TEXT),
            (cls.TR_HAMMER_COUNT, SQLType.INTEGER),
            (cls.TR_MC_EFFECT_MEASURES_LIST, SQLType.JSONB_DEFAULT_EMPTY_ARRAY),
            (cls.TR_PAC_MEASURES_LIST, SQLType.JSONB_DEFAULT_EMPTY_ARRAY),
            (cls.TR_OPENING_KEY, SQLType.TEXT),
            (cls.TR_OTHER_KEYS_LIST, SQLType.TEXT),
            (cls.TR_ENDING_KEY, SQLType.TEXT),
            (cls.TR_ENDING_CADENCE, SQLType.TEXT),

        ]

    @classmethod
    def _mc_field_sql_type_list(cls) -> List[Tuple[Field, SQLType]]:
        return [
            (cls.MC_PRESENT, SQLType.BOOLEAN_DEFAULT_TRUE),
            (cls.MC_MEASURES, SQLType.TEXT),
            (cls.MC_DYNAMICS, SQLType.TEXT),
            (cls._MC_TYPE, SQLType.TEXT),  # Derived field so never specify it
            (cls.MC_COMMENTS, SQLType.TEXT),
            (cls.MC_STYLE, SQLType.TEXT),
            (cls.MC_FILL_KEY, SQLType.TEXT),
        ]

    @classmethod
    def _s_field_sql_type_list(cls) -> List[Tuple[Field, SQLType]]:
        return [
            (cls.S_PRESENT, SQLType.BOOLEAN_DEFAULT_TRUE),
            (cls.S_MEASURES, SQLType.TEXT),
            (cls.S_COMMENTS, SQLType.TEXT),
            (cls.S_TYPE, SQLType.TEXT),
            (cls.S_MODULE_MEASURES_DICT, SQLType.JSONB),
            (cls.S_MODULE_TYPES_DICT, SQLType.JSONB),
            (cls.S_MODULE_PHRASE_DICT, SQLType.JSONB),
            (cls.S_MODULE_DYNAMICS_DICT, SQLType.JSONB),
            (cls.S_STRONG_PAC_MEAS_LIST, SQLType.JSONB_DEFAULT_EMPTY_ARRAY),
            (cls.S_ATTEN_PAC_MEAS_LIST, SQLType.JSONB_DEFAULT_EMPTY_ARRAY),
            (cls.S_EVADED_PAC_MEAS_LIST, SQLType.JSONB_DEFAULT_EMPTY_ARRAY),
            (cls.S_OPENING_KEY, SQLType.TEXT),
            (cls.S_OTHER_KEYS_LIST, SQLType.JSONB),
            (cls.S_ENDING_KEY, SQLType.TEXT),
            (cls.S_ENDING_CADENCE, SQLType.TEXT),
            (cls.EEC_ESC_SECURED, SQLType.BOOLEAN_DEFAULT_TRUE),
            (cls.EEC_ESC_MEASURE, SQLType.TEXT),
            (cls.EEC_ESC_COMMENTS, SQLType.TEXT),
            (cls.EEC_ESC_DYNAMICS, SQLType.TEXT),
        ]

    @classmethod
    def _c_field_sql_type_list(cls) -> List[Tuple[Field, SQLType]]:
        return [
            (cls.C_PRESENT, SQLType.BOOLEAN_DEFAULT_TRUE),
            (cls.C_SC_PRE_EEC_ESC, SQLType.BOOLEAN_DEFAULT_FALSE),
            (cls.C_MEASURES_INCL_C_RT, SQLType.TEXT),
            (cls.C_COMMENTS, SQLType.TEXT),
            (cls.C_TYPE, SQLType.TEXT),
            (cls.C_MODULE_MEASURES_DICT, SQLType.JSONB),
            (cls.C_MODULE_TYPES_DICT, SQLType.JSONB),
            (cls.C_MODULE_PHRASE_DICT, SQLType.JSONB),
            (cls.C_MODULE_DYNAMICS_DICT, SQLType.JSONB),
            (cls.C_PAC_MEASURES_LIST, SQLType.JSONB_DEFAULT_EMPTY_ARRAY),
            (cls.C_OPENING_KEY, SQLType.TEXT),
            (cls.C_OTHER_KEYS_LIST, SQLType.JSONB),
            (cls.C_ENDING_KEY_BEFORE_C_RT, SQLType.TEXT),
            (cls.C_RT_PRESENT, SQLType.BOOLEAN_DEFAULT_FALSE),
            (cls.C_RT_MEASURES, SQLType.TEXT),
            (cls.C_RT_ENDING_KEY, SQLType.TEXT),
            (cls.C_RT_DYNAMICS, SQLType.TEXT),
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
    COMMENTS = Field("comments", "Development Comments")
    OPENING_TEMPO = Field("opening_tempo", "Opening Tempo")
    OPENING_KEY = Field("opening_key", "Development Opening Key")
    OTHER_KEYS_LIST = Field("other_keys", "Development Other Key(s)")
    # JSONArray of all keys IN ORDER between opening key and ending key

    # Episodes
    NUM_EPISODES = Field("num_episodes", "Development Episodes")
    EPISODE_MEASURES_DICT = Field("episode_measures", "Episode Measures")  # a map of episode to a measure range
    EPISODE_DESCRIPTIONS_DICT = Field("episode_descriptions", "Episode Description")
    EPISODE_TONAL_DICT = Field("episode_tonal_map", "Episode Tonal Map")  # a map of episode to the keys used
    EPISODE_THEME_DICT = Field("episode_theme_map",
                               "Episode Theme Map")  # a map of episode to the themes used P / S / TR / C

    P_INITIATED = Field("p_theme_initiated", "P Theme Initiated")
    P_DEVELOPED = Field("p_theme_developed", "P Theme Developed")
    TR_DEVELOPED = Field("tr_theme_developed", "TR Theme Developed")
    S_DEVELOPED = Field("s_theme_developed", "S Theme Developed")
    C_DEVELOPED = Field("c_theme_developed", "C Theme Developed")

    # Development Theme
    DEVELOPMENT_THEME_PRESENT = Field("development_theme_present", "Development New Theme Present")
    DEVELOPMENT_THEME_KEYS = Field("development_theme_keys", "Development New Theme Keys")
    DEVELOPMENT_THEME_COMMENTS = Field("Development Theme Comments")

    # Retransition
    ENDING_KEY = Field("ending_key", "Development Ending Key")
    ENDING_CADENCE = Field("ending_cadence", "Development Ending Cadence")

    @classmethod
    def absolute_key_fields(cls) -> Set[Field]:
        return {
            cls.OPENING_KEY,
            cls.OTHER_KEYS_LIST,
            cls.DEVELOPMENT_THEME_KEYS,
            cls.ENDING_KEY,
        }

    @classmethod
    def measure_range_fields_to_compute_measure_counts(cls) -> Set[Field]:
        return {
            cls.MEASURES,
            cls.EPISODE_MEASURES_DICT,
        }

    @classmethod
    def measures_array_fields_to_compute_counts(cls) -> Set[Field]:
        return set()

    @classmethod
    def field_sql_type_list_pre_derived_fields(cls) -> List[Tuple[Field, SQLType]]:
        return [
            (cls.ID, SQLType.TEXT_PRIMARY_KEY),
            (cls.SONATA_ID, SQLType.TEXT),
            (cls.MEASURES, SQLType.TEXT),
            (cls.NUM_CYCLES, SQLType.INTEGER),
            (cls.DEVELOPMENT_TYPE, SQLType.TEXT),
            (cls.COMMENTS, SQLType.TEXT),
            (cls.OPENING_TEMPO, SQLType.TEXT),
            (cls.OPENING_KEY, SQLType.TEXT),

            (cls.OTHER_KEYS_LIST, SQLType.JSONB),  # JSONArray

            # Episodes
            (cls.NUM_EPISODES, SQLType.INTEGER),
            (cls.EPISODE_MEASURES_DICT, SQLType.JSONB),
            (cls.EPISODE_DESCRIPTIONS_DICT, SQLType.JSONB),
            (cls.EPISODE_THEME_DICT, SQLType.JSONB),
            (cls.EPISODE_TONAL_DICT, SQLType.JSONB),

            (cls.P_INITIATED, SQLType.BOOLEAN),
            (cls.P_DEVELOPED, SQLType.BOOLEAN),
            (cls.TR_DEVELOPED, SQLType.BOOLEAN),
            (cls.S_DEVELOPED, SQLType.BOOLEAN),
            (cls.C_DEVELOPED, SQLType.BOOLEAN),

            # Development Theme
            (cls.DEVELOPMENT_THEME_PRESENT, SQLType.BOOLEAN),
            (cls.DEVELOPMENT_THEME_KEYS, SQLType.JSONB),
            (cls.DEVELOPMENT_THEME_COMMENTS, SQLType.TEXT),

            (cls.ENDING_KEY, SQLType.TEXT),
            (cls.ENDING_CADENCE, SQLType.TEXT),
        ]


class Recap(Expo):
    """
    The table representing items particular to the recapitulation block in a sonata.

    Inherits from the Exposition since in general everything in the Exposition we want in the recap
    """

    @classmethod
    def schema_table(cls) -> SchemaTable:
        return SchemaTable(sonata_archives_schema, "sonata_recapitulation")

    # Override the display names on these exposition attributes
    MEASURES = Expo.MEASURES.clone_with_new_display_name("Recapitulation Measures")
    NUM_CYCLES = Expo.NUM_CYCLES.clone_with_new_display_name("Recapitulation Number of Cycles")
    # does not include literal exposition repeats

    CONTINUOUS = Expo.CONTINUOUS.clone_with_new_display_name("Continuous Recapitulation")
    CONTINUOUS_SUBTYPE = Expo.CONTINUOUS_SUBTYPE.clone_with_new_display_name("Continuous Recapitulation Subtype")
    DUTCHMAN_TYPE = Expo.DUTCHMAN_TYPE.clone_with_new_display_name( "Dutchman-Type Recapitulation")
    # Apotheosis of S as redemptive agent
    COMMENTS = Expo.COMMENTS.clone_with_new_display_name("Recapitulation Comments")
    OPENING_TEMPO = Expo.OPENING_TEMPO.clone_with_new_display_name("Recapitulation Opening Tempo")

    # Add some new attributes and override others to change the name
    FALSE_CRUX_MEASURES = Field("false_crux_measures", "False Crux Measures")
    CRUX_MEASURE = Field("crux_measure", "Crux Measure")

    # P
    P_PRESENT = Field("p_theme_present", "P Theme Present")  # Type 2 Sonatas don't recap P
    P_COMMENTS = Expo.P_COMMENTS.clone_with_new_display_name("P Theme Change From Exposition")

    # TR
    TR_COMMENTS = Expo.TR_COMMENTS.clone_with_new_display_name("TR Theme Change From Exposition")

    # MC
    MC_COMMENTS = Expo.MC_COMMENTS.clone_with_new_display_name("MC Change from Exposition")

    # S
    S_COMMENTS = Expo.S_COMMENTS.clone_with_new_display_name("S Theme Change From Exposition")

    # ESC
    # Only fill this field if ESC is not secured, which indicates whether there is any "wrong-key" substitute or not
    # If true, then the eec_esc_measure refers to the false esc, since the real one was not secured
    # Override the display name since EEC vs ESC only core sonata thing named differently between the two halfs
    EEC_ESC_SECURED = Expo.EEC_ESC_SECURED.clone_with_new_display_name("ESC Secured")
    EEC_ESC_MEASURE = Expo.EEC_ESC_MEASURE.clone_with_new_display_name("ESC Measure")
    EEC_ESC_COMMENTS = Expo.EEC_ESC_COMMENTS.clone_with_new_display_name("ESC Change From EEC")
    EEC_ESC_DYNAMICS = Expo.EEC_ESC_DYNAMICS.clone_with_new_display_name("ESC Dynamics")
    ESC_FALSE_SUBSTITUTE = Field("esc_false_substitute", "ESC False/Substitute")

    # C
    C_SC_PRE_EEC_ESC = Expo.C_SC_PRE_EEC_ESC.clone_with_new_display_name("C Theme SC / Pre-ESC")
    C_COMMENTS = Expo.C_COMMENTS.clone_with_new_display_name("C Theme Change From Exposition")

    # Builds this by using Exposition parent's lists with ability to add additional below each one
    # (This enables the new Recap elements to not have to be all at the end
    @classmethod
    def field_sql_type_list_pre_derived_fields(cls) -> List[Tuple[Field, SQLType]]:
        list_of_lists = [
            cls._general_field_sql_type_list(),
            [
                (cls.FALSE_CRUX_MEASURES, SQLType.JSONB_DEFAULT_EMPTY_ARRAY),
                (cls.CRUX_MEASURE, SQLType.TEXT),
                (cls.P_PRESENT, SQLType.BOOLEAN_DEFAULT_TRUE),
            ],
            cls._p_field_sql_type_list(),
            [
            ],

            cls._tr_field_sql_type_list(),
            [
            ],

            cls._mc_field_sql_type_list(),
            [
            ],

            cls._s_field_sql_type_list(),
            [
                (cls.ESC_FALSE_SUBSTITUTE, SQLType.BOOLEAN_DEFAULT_FALSE),
            ],

            cls._c_field_sql_type_list(),
            [
            ],
        ]
        # Flatten list of lists
        return [item for sublist in list_of_lists for item in sublist]


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
    COMMENTS = Field("comments", "Coda Comments")
    OPENING_TEMPO = Field("opening_tempo", "Coda Opening Tempo")
    OPENING_KEY = Field("opening_key", "Coda Opening Key")

    OTHER_KEYS_LIST = Field("other_keys", "Coda Other Key(s)")  # a JSONArray of keys tonicized
    P_RECALLED = Field("p_theme_recalled", "P Theme Recalled")
    TR_RECALLED = Field("tr_theme_recalled", "TR Theme Recalled")
    S_RECALLED = Field("s_theme_recalled", "S Theme Recalled")
    C_RECALLED = Field("c_theme_recalled", "C Theme Recalled")
    INTRODUCTION_THEME_RECALLED = Field("introduction_theme_recalled", "Introduction Theme Recalled")
    DEVELOPMENT_THEME_RECALLED = Field("development_theme_recalled", "Development New Theme Recalled")

    ENDING_KEY = Field("ending_key", "Coda Ending Key")
    ENDING_CADENCE = Field("ending_cadence", "Coda Ending Cadence")

    @classmethod
    def absolute_key_fields(cls) -> Set[Field]:
        return {
            cls.OPENING_KEY,
            cls.ENDING_KEY,
        }

    @classmethod
    def measure_range_fields_to_compute_measure_counts(cls) -> Set[Field]:
        return {
            cls.MEASURES
        }

    @classmethod
    def measures_array_fields_to_compute_counts(cls) -> Set[Field]:
        return set()

    @classmethod
    def field_sql_type_list_pre_derived_fields(cls) -> List[Tuple[Field, SQLType]]:
        return [
            (cls.ID, SQLType.TEXT_PRIMARY_KEY),
            (cls.SONATA_ID, SQLType.TEXT),
            (cls.NUM_CYCLES, SQLType.INTEGER),
            (cls.MEASURES, SQLType.TEXT),
            (cls.CODA_TYPE, SQLType.TEXT),
            (cls.COMMENTS, SQLType.TEXT),
            (cls.OPENING_TEMPO, SQLType.TEXT),
            (cls.OPENING_KEY, SQLType.TEXT),

            (cls.OTHER_KEYS_LIST, SQLType.JSONB),  # JSONArray
            (cls.P_RECALLED, SQLType.BOOLEAN),
            (cls.TR_RECALLED, SQLType.BOOLEAN),
            (cls.S_RECALLED, SQLType.BOOLEAN),
            (cls.C_RECALLED, SQLType.BOOLEAN),
            (cls.INTRODUCTION_THEME_RECALLED, SQLType.BOOLEAN),
            (cls.DEVELOPMENT_THEME_RECALLED, SQLType.BOOLEAN),

            (cls.ENDING_KEY, SQLType.TEXT),
            (cls.ENDING_CADENCE, SQLType.TEXT),
        ]
