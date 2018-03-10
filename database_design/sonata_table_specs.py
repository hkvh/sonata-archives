#!/usr/bin/env python
"""
A module containing the specification for the base SQL tables (and views, which act like tables)
"""
from abc import abstractmethod, ABC
from typing import Tuple, List, Set

from psycopg2 import sql

from database_design.table_spec import TableSpecification
from general_utils.sql_utils import Field, SQLType, SchemaTable, Schema

sonata_archives_schema = Schema("sonata_archives")


class Composer(TableSpecification):
    """
    The table that stores information about composers
    """

    @classmethod
    def schema_table(cls) -> SchemaTable:
        return SchemaTable(sonata_archives_schema, "composer")

    ID = Field("id")
    FULL_NAME = Field("full_name")
    SURNAME = Field("surname")
    NATIONALITY = Field("nationality")
    BIRTH_DATE = Field("birth_date")
    DEATH_DATE = Field("death_date")
    BIRTHPLACE = Field("birthplace")
    PRIMARY_RESIDENCE = Field("primary_residence")

    @classmethod
    def field_sql_type_list(cls) -> List[Tuple[Field, SQLType]]:
        return [
            (cls.ID, SQLType.TEXT()),
            (cls.FULL_NAME, SQLType.TEXT()),
            (cls.SURNAME, SQLType.TEXT()),
            (cls.NATIONALITY, SQLType.TEXT()),
            (cls.BIRTH_DATE, SQLType.DATE()),
            (cls.DEATH_DATE, SQLType.DATE()),
            (cls.BIRTHPLACE, SQLType.TEXT()),
            (cls.PRIMARY_RESIDENCE, SQLType.TEXT()),
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
    NAME = Field("name")
    CATALOGUE_ID = Field("catalogue_id")  # K. for mozart, D. for schubert, Op. and No. for most composers
    NICKNAME = Field("nickname")
    FULL_NAME = Field("full_name")  # usually don't enter this, let it be derived from name, cat_id and nickname
    PIECE_TYPE = Field("piece_type")  # Symphony vs. Piano Sonata etc.
    YEAR_STARTED = Field("year_started")
    YEAR_COMPLETED = Field("year_completed")
    PREMIER_DATE = Field("premier_date")
    GLOBAL_KEY = Field("global_key")
    NUM_MOVEMENTS = Field("num_movements")

    @classmethod
    def field_sql_type_list(cls) -> List[Tuple[Field, SQLType]]:
        return [
            (cls.ID, SQLType.TEXT()),
            (cls.COMPOSER_ID, SQLType.TEXT()),
            (cls.NAME, SQLType.TEXT()),
            (cls.CATALOGUE_ID, SQLType.TEXT()),
            (cls.NICKNAME, SQLType.TEXT()),
            (cls.FULL_NAME, SQLType.TEXT()),
            (cls.PIECE_TYPE, SQLType.TEXT()),
            (cls.YEAR_STARTED, SQLType.INTEGER()),
            (cls.YEAR_COMPLETED, SQLType.INTEGER()),
            (cls.PREMIER_DATE, SQLType.DATE()),
            (cls.GLOBAL_KEY, SQLType.TEXT()),
            (cls.NUM_MOVEMENTS, SQLType.INTEGER()),
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
    MOVEMENT_NUM = Field("movement_num")
    SONATA_TYPE = Field("sonata_type")  # Sonata Theory Types 1-5
    GLOBAL_KEY = Field("global_key")
    EXPOSITION_REPEAT = Field("exposition_repeat")
    DEVELOPMENT_RECAP_REPEAT = Field("development_recap_repeat")
    INTRODUCTION_PRESENT = Field("introduction_present")
    DEVELOPMENT_PRESENT = Field("development_present")
    CODA_PRESENT = Field("coda_present")
    INTRODUCTION_ID = Field("introduction_id")
    EXPOSITION_ID = Field("exposition_id")
    DEVELOPMENT_ID = Field("development_id")
    RECAPITULATION_ID = Field("recapitulation_id")
    CODA_ID = Field("coda_id")

    @classmethod
    def field_sql_type_list(cls) -> List[Tuple[Field, SQLType]]:
        return [
            (cls.ID, SQLType.TEXT()),
            (cls.PIECE_ID, SQLType.TEXT()),
            (cls.MOVEMENT_NUM, SQLType.INTEGER()),
            (cls.SONATA_TYPE, SQLType.TEXT()),
            (cls.GLOBAL_KEY, SQLType.TEXT()),
            (cls.EXPOSITION_REPEAT, SQLType.BOOLEAN()),
            (cls.DEVELOPMENT_RECAP_REPEAT, SQLType.BOOLEAN()),
            (cls.INTRODUCTION_PRESENT, SQLType.BOOLEAN()),
            (cls.DEVELOPMENT_PRESENT, SQLType.BOOLEAN()),
            (cls.CODA_PRESENT, SQLType.BOOLEAN()),
            (cls.INTRODUCTION_ID, SQLType.TEXT()),
            (cls.EXPOSITION_ID, SQLType.TEXT()),
            (cls.DEVELOPMENT_ID, SQLType.TEXT()),
            (cls.RECAPITULATION_ID, SQLType.TEXT()),
            (cls.CODA_ID, SQLType.TEXT()),
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

    @classmethod
    @abstractmethod
    def absolute_key_fields(cls) -> Set[Field]:
        """
        Returns a set of all absolute key fields, which will be the set of fields for which we will add a
        corresponding relative key.

        :return: a set of fields corresponding to all the fields that are for absolute keys
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

    @staticmethod
    def get_relative_from_absolute(absolute_key_field: Field) -> Field:
        """
        Given a field name with the word key, dynamically replaces it with relative key.
        :param absolute_key_field: the name of the absolute key field. Must contain the word "key"
        :return: a new Field with key switched out for relative key as its name
        """
        field_name = absolute_key_field.name
        if 'key' not in field_name:
            raise Exception("Field {} marked as an absolute key field but didn't contain \"key\"")
        else:
            return Field(field_name.replace('key', 'relative_key'))

    @classmethod
    def field_sql_type_list(cls) -> List[Tuple[Field, SQLType]]:
        """
        We override this to add in derived fields from the preliminary list created in the pre_derived field list.

        Right now, the only derived fields are the relative keys built from every absolute key field specified in
        absolute_key_fields using the staticmethod get_relative_from_absolute.

        :return: a list of tuple pairs of fields with their sql type in the ordinal order that we want them in the table
        """

        new_list = []
        for field, sql_type in cls.field_sql_type_list_pre_derived_fields():

            new_list.append((field, sql_type))

            # If any field is in the set of absolute key fields, add the relative key version of it right afterwards
            if field in cls.absolute_key_fields():
                if sql_type != SQLType.TEXT():
                    raise Exception("Field \"{}\" in class {} was marked as an absolute key field, which means it "
                                    "should have a SQLType of TEXT instead of {}"
                                    "".format(field.name, cls.__name__, sql_type))
                relative_key_field = cls.get_relative_from_absolute(field)
                new_list.append((relative_key_field, SQLType.TEXT()))

        return new_list


class Introduction(SonataBlockTableSpecification):
    """
    The table representing items particular to the introduction block in a sonata.
    """

    @classmethod
    def schema_table(cls) -> SchemaTable:
        return SchemaTable(sonata_archives_schema, "sonata_introduction")

    NUM_CYCLES = Field("num_cycles")

    INTRODUCTION_TYPE = Field("introduction_type")
    OPENING_KEY = Field("opening_key")

    OPENING_TEMPO = Field("opening_tempo")
    KEYS_TONICIZED = Field("keys_tonicized")  # a JSONArray of keys tonicized
    P_THEME_FORESHADOWED = Field("p_theme_recalled")
    TR_THEME_FORESHADOWED = Field("tr_theme_foreshadowed")
    S_THEME_FORESHADOWED = Field("s_theme_foreshadowed")
    C_THEME_FORESHADOWED = Field("c_theme_foreshadowed")

    # I
    INTRO_THEME_PRESENT = Field("intro_theme_present")  # whether the intro contains a novel theme
    INTRO_THEME_KEY = Field("intro_theme_key")
    INTRO_THEME_DESCRIPTION = Field("intro_theme_description")
    INTRO_THEME_MOTIVES_LILYPOND = Field("intro_theme_motives_lilypond")

    ENDING_KEY = Field("ending_key")
    ENDING_CADENCE = Field("ending_cadence")

    @classmethod
    def absolute_key_fields(cls) -> Set[Field]:
        return {
            cls.OPENING_KEY,
            cls.INTRO_THEME_KEY,
            cls.ENDING_KEY,
        }

    @classmethod
    def field_sql_type_list_pre_derived_fields(cls) -> List[Tuple[Field, SQLType]]:
        return [
            (cls.ID, SQLType.TEXT()),
            (cls.NUM_CYCLES, SQLType.INTEGER()),

            (cls.INTRODUCTION_TYPE, SQLType.TEXT()),
            (cls.OPENING_KEY, SQLType.TEXT()),
            (cls.OPENING_TEMPO, SQLType.TEXT()),
            (cls.KEYS_TONICIZED, SQLType.JSONB()),  # JSONArray
            (cls.P_THEME_FORESHADOWED, SQLType.BOOLEAN()),
            (cls.TR_THEME_FORESHADOWED, SQLType.BOOLEAN()),
            (cls.S_THEME_FORESHADOWED, SQLType.BOOLEAN()),
            (cls.C_THEME_FORESHADOWED, SQLType.BOOLEAN()),

            # I Theme
            (cls.INTRO_THEME_PRESENT, SQLType.BOOLEAN()),
            (cls.INTRO_THEME_KEY, SQLType.TEXT()),
            (cls.INTRO_THEME_DESCRIPTION, SQLType.TEXT()),
            (cls.INTRO_THEME_MOTIVES_LILYPOND, SQLType.JSONB()),

            (cls.ENDING_KEY, SQLType.TEXT()),
            (cls.ENDING_CADENCE, SQLType.TEXT()),
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

    NUM_CYCLES = Field("num_cycles")  # does not include literal exposition repeats -- see sonata method
    OPENING_TEMPO = Field("opening_tempo")

    # P
    P_THEME_KEY = Field("p_theme_key")
    P_THEME_DESCRIPTION = Field("p_theme_description")
    P_THEME_PHRASE_STRUCTURE = Field("p_theme_phrase_structure")
    P_THEME_MOTIVES_LILYPOND = Field("p_theme_motives_lilypond")
    P_THEME_ENDING_KEY = Field("p_theme_ending_key")
    P_THEME_ENDING_CADENCE = Field("p_theme_ending_cadence")

    # TR
    TR_THEME_PRESENT = Field("tr_theme_present")
    TR_THEME_KEY = Field("tr_theme_key")
    TR_THEME_DESCRIPTION = Field("tr_theme_description")
    TR_THEME_P_BASED = Field("tr_theme_p_based")
    TR_THEME_PHRASE_STRUCTURE = Field("tr_theme_phrase_structure")
    TR_THEME_MOTIVES_LILYPOND = Field("tr_theme_motives_lilypond")
    TR_THEME_ENERGY_GAIN = Field("tr_theme_energy_gain")
    TR_THEME_HAMMER_BLOWS = Field("tr_theme_hammer_blows")
    TR_THEME_ENDING_KEY = Field("tr_theme_ending_key")
    TR_THEME_ENDING_CADENCE = Field("tr_theme_ending_cadence")

    # MC
    MC_PRESENT = Field("mc_present")
    MC_TYPE = Field("mc_type")

    # S
    S_THEME_PRESENT = Field("s_theme_present")
    S_THEME_KEY = Field("s_theme_key")
    S_THEME_DESCRIPTION = Field("s_theme_description")
    S_THEME_P_BASED = Field("s_theme_p_based")
    S_THEME_PHRASE_STRUCTURE = Field("s_theme_phrase_structure")
    S_THEME_MOTIVES_LILYPOND = Field("s_theme_motives_lilypond")
    S_THEME_ENDING_KEY = Field("s_theme_ending_key")
    S_THEME_ENDING_CADENCE = Field("s_theme_ending_cadence")

    # EEC
    EEC_PRESENT = Field("eec_present")
    EEC_FAKED_OUT_COUNT = Field("eec_fake_out_count")
    EEC_STRENGTH = Field("eec_strength")

    # C
    C_THEME_PRESENT = Field("c_theme_present")
    C_THEME_KEY = Field("c_theme_key")
    C_THEME_DESCRIPTION = Field("c_theme_description")
    C_THEME_P_BASED = Field("c_theme_p_based")
    C_THEME_S_BASED = Field("c_theme_s_based")
    C_THEME_PHRASE_STRUCTURE = Field("c_theme_phrase_structure")
    C_THEME_MOTIVES_LILYPOND = Field("c_theme_motives_lilypond")
    C_THEME_ENDING_KEY = Field("c_theme_ending_key")

    @classmethod
    def absolute_key_fields(cls) -> Set[Field]:
        return {
            cls.P_THEME_KEY,
            cls.P_THEME_ENDING_KEY,
            cls.TR_THEME_KEY,
            cls.TR_THEME_ENDING_KEY,
            cls.S_THEME_KEY,
            cls.S_THEME_ENDING_KEY,
            cls.C_THEME_KEY,
            cls.C_THEME_ENDING_KEY
        }

    @classmethod
    def field_sql_type_list_pre_derived_fields(cls) -> List[Tuple[Field, SQLType]]:
        return [
            (cls.ID, SQLType.TEXT()),
            (cls.NUM_CYCLES, SQLType.INTEGER()),
            (cls.OPENING_TEMPO, SQLType.TEXT()),

            # P
            (cls.P_THEME_KEY, SQLType.TEXT()),
            (cls.P_THEME_DESCRIPTION, SQLType.TEXT()),
            (cls.P_THEME_PHRASE_STRUCTURE, SQLType.JSONB()),
            (cls.P_THEME_MOTIVES_LILYPOND, SQLType.JSONB()),
            (cls.P_THEME_ENDING_KEY, SQLType.TEXT()),
            (cls.P_THEME_ENDING_CADENCE, SQLType.TEXT()),

            # TR
            (cls.TR_THEME_PRESENT, SQLType.BOOLEAN()),
            (cls.TR_THEME_KEY, SQLType.TEXT()),
            (cls.TR_THEME_DESCRIPTION, SQLType.TEXT()),
            (cls.TR_THEME_P_BASED, SQLType.BOOLEAN()),
            (cls.TR_THEME_PHRASE_STRUCTURE, SQLType.JSONB()),
            (cls.TR_THEME_MOTIVES_LILYPOND, SQLType.TEXT()),
            (cls.TR_THEME_ENERGY_GAIN, SQLType.BOOLEAN()),
            (cls.TR_THEME_HAMMER_BLOWS, SQLType.BOOLEAN()),
            (cls.TR_THEME_ENDING_KEY, SQLType.TEXT()),
            (cls.TR_THEME_ENDING_CADENCE, SQLType.TEXT()),

            # MC
            (cls.MC_PRESENT, SQLType.BOOLEAN()),
            (cls.MC_TYPE, SQLType.TEXT()),

            # S
            (cls.S_THEME_PRESENT, SQLType.TEXT()),
            (cls.S_THEME_KEY, SQLType.TEXT()),
            (cls.S_THEME_DESCRIPTION, SQLType.TEXT()),
            (cls.S_THEME_P_BASED, SQLType.TEXT()),
            (cls.S_THEME_PHRASE_STRUCTURE, SQLType.TEXT()),
            (cls.S_THEME_MOTIVES_LILYPOND, SQLType.JSONB()),
            (cls.S_THEME_ENDING_KEY, SQLType.TEXT()),
            (cls.S_THEME_ENDING_CADENCE, SQLType.TEXT()),

            # EEC
            (cls.EEC_PRESENT, SQLType.BOOLEAN()),
            (cls.EEC_FAKED_OUT_COUNT, SQLType.INTEGER()),
            (cls.EEC_STRENGTH, SQLType.TEXT()),

            # C
            (cls.C_THEME_PRESENT, SQLType.BOOLEAN()),
            (cls.C_THEME_KEY, SQLType.TEXT()),
            (cls.C_THEME_DESCRIPTION, SQLType.TEXT()),
            (cls.C_THEME_P_BASED, SQLType.TEXT()),
            (cls.C_THEME_S_BASED, SQLType.TEXT()),
            (cls.C_THEME_PHRASE_STRUCTURE, SQLType.JSONB()),
            (cls.C_THEME_MOTIVES_LILYPOND, SQLType.JSONB()),
            (cls.C_THEME_ENDING_KEY, SQLType.TEXT()),
        ]

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

    NUM_CYCLES = Field("num_cycles")

    DEVELOPMENT_TYPE = Field("development_type")
    OPENING_KEY = Field("opening_key")
    OPENING_TEMPO = Field("opening_tempo")
    KEYS_TONICIZED = Field("keys_tonicized")  # a JSONArray of all keys tonicized in the development

    # Episodes
    NUM_EPISODES = Field("num_episodes")
    EPISODE_DESCRIPTIONS = Field("episode_descriptions")
    EPISODE_TONAL_MAP = Field("episode_tonal_map")  # a map of episode to the keys used
    EPISODE_THEME_MAP = Field("episode_theme_map")  # a map of episode to the themes used P / S / TR / C
    EPISODE_MOTIVE_LILYPOND = Field("episode_motive_lilypond")  # motives of each development episode

    P_THEME_INITIATED = Field("p_theme_initiated")
    P_THEME_DEVELOPED = Field("p_theme_developed")
    TR_THEME_DEVELOPED = Field("tr_theme_developed")
    S_THEME_DEVELOPED = Field("s_theme_developed")
    C_THEME_DEVELOPED = Field("c_theme_developed")

    # Development Theme
    DEVELOPMENT_THEME_PRESENT = Field("development_theme_present")  # whether the development contains a novel theme
    DEVELOPMENT_THEME_KEY = Field("coda_theme_key")
    DEVELOPMENT_THEME_DESCRIPTION = Field("coda_theme_description")
    DEVELOPMENT_THEME_MOTIVES = Field("development_theme_motives_lilypond")

    # Retransition
    RETRANSITION_PRESENT = Field("retransition_present")
    RETRANSITION_ENDING_KEY = Field("retransition_ending_key")
    RETRANSITION_ENDING_CADENCE = Field("retransition_ending_cadence")

    @classmethod
    def absolute_key_fields(cls) -> Set[Field]:
        return {
            cls.OPENING_KEY,
            cls.DEVELOPMENT_THEME_KEY,
            cls.RETRANSITION_ENDING_KEY,
        }

    @classmethod
    def field_sql_type_list_pre_derived_fields(cls) -> List[Tuple[Field, SQLType]]:
        return [
            (cls.ID, SQLType.TEXT()),
            (cls.NUM_CYCLES, SQLType.INTEGER()),

            (cls.DEVELOPMENT_TYPE, SQLType.TEXT()),
            (cls.OPENING_KEY, SQLType.TEXT()),
            (cls.OPENING_TEMPO, SQLType.TEXT()),
            (cls.KEYS_TONICIZED, SQLType.JSONB()),  # JSONArray

            # Episodes
            (cls.NUM_EPISODES, SQLType.INTEGER()),
            (cls.EPISODE_DESCRIPTIONS, SQLType.JSONB()),
            (cls.EPISODE_THEME_MAP, SQLType.JSONB()),
            (cls.EPISODE_TONAL_MAP, SQLType.JSONB()),
            (cls.EPISODE_MOTIVE_LILYPOND, SQLType.JSONB()),

            (cls.P_THEME_INITIATED, SQLType.BOOLEAN()),
            (cls.P_THEME_DEVELOPED, SQLType.BOOLEAN()),
            (cls.TR_THEME_DEVELOPED, SQLType.BOOLEAN()),
            (cls.S_THEME_DEVELOPED, SQLType.BOOLEAN()),
            (cls.C_THEME_DEVELOPED, SQLType.BOOLEAN()),

            # Development Theme
            (cls.DEVELOPMENT_THEME_PRESENT, SQLType.BOOLEAN()),
            (cls.DEVELOPMENT_THEME_KEY, SQLType.TEXT()),
            (cls.DEVELOPMENT_THEME_DESCRIPTION, SQLType.TEXT()),
            (cls.DEVELOPMENT_THEME_MOTIVES, SQLType.JSONB()),

            (cls.RETRANSITION_PRESENT, SQLType.BOOLEAN()),
            (cls.RETRANSITION_ENDING_KEY, SQLType.TEXT()),
            (cls.RETRANSITION_ENDING_CADENCE, SQLType.TEXT()),
        ]

    @classmethod
    def create_constraints_sql(cls) -> sql.Composable:
        return sql.SQL("ALTER TABLE {st} ADD PRIMARY KEY ({id});").format(st=cls.schema_table(), id=cls.ID)


class Recapitulation(SonataBlockTableSpecification):
    """
    The table representing items particular to the recapitulation block in a sonata.
    """

    @classmethod
    def schema_table(cls) -> SchemaTable:
        return SchemaTable(sonata_archives_schema, "sonata_recapitulation")

    NUM_CYCLES = Field("num_cycles")  # does not include literal recap + development repeats -- see sonata method
    OPENING_TEMPO = Field("opening_tempo")

    # P
    P_THEME_KEY = Field("p_theme_key")
    P_THEME_DESCRIPTION = Field("p_theme_description")
    P_THEME_CHANGE_FROM_EXPOSITION = Field("p_theme_change_from_exposition")
    P_THEME_MOTIVES_LILYPOND = Field("p_theme_motives_lilypond")  # if changed significantly from exposition
    P_THEME_ENDING_KEY = Field("p_theme_ending_key")
    P_THEME_ENDING_CADENCE = Field("p_theme_ending_cadence")

    # TR
    TR_THEME_PRESENT = Field("tr_theme_present")
    TR_THEME_KEY = Field("tr_theme_key")
    TR_THEME_DESCRIPTION = Field("tr_theme_description")
    TR_THEME_CHANGE_FROM_EXPOSITION = Field("tr_theme_change_from_exposition")
    TR_THEME_MOTIVES_LILYPOND = Field("tr_theme_motives_lilypond")  # if changed significantly from exposition
    TR_THEME_ENDING_KEY = Field("tr_theme_ending_key")
    TR_THEME_ENDING_CADENCE = Field("tr_theme_ending_cadence")

    # MC
    MC_PRESENT = Field("mc_present")
    MC_CHANGE_FROM_EXPOSITION = Field("mc_change_from_exposition")

    # S
    S_THEME_PRESENT = Field("s_theme_present")
    S_THEME_KEY = Field("s_theme_key")
    S_THEME_DESCRIPTION = Field("s_theme_description")
    S_THEME_CHANGE_FROM_EXPOSITION = Field("s_theme_change_from_exposition")
    S_THEME_MOTIVES_LILYPOND = Field("s_theme_motives_lilypond")  # if changed significantly from exposition
    S_THEME_ENDING_KEY = Field("s_theme_ending_key")
    S_THEME_ENDING_CADENCE = Field("s_theme_ending_cadence")

    # EEC
    ESC_PRESENT = Field("esc_present")
    ESC_FAKED_OUT_COUNT = Field("eec_fake_out_count")
    ESC_STRENGTH = Field("esc_strength")
    ESC_CHANGE_FROM_EXPOSITION = Field("esc_change_from_exposition")

    # C
    C_THEME_PRESENT = Field("c_theme_present")
    C_THEME_KEY = Field("c_theme_key")
    C_THEME_DESCRIPTION = Field("c_theme_description")
    C_THEME_CHANGE_FROM_EXPOSITION = Field("c_theme_change_from_exposition")
    C_THEME_MOTIVES_LILYPOND = Field("c_theme_motives_lilypond")  # if changed significantly from exposition
    C_THEME_ENDING_KEY = Field("c_theme_ending_key")

    @classmethod
    def absolute_key_fields(cls) -> Set[Field]:
        return {
            cls.P_THEME_KEY,
            cls.P_THEME_ENDING_KEY,
            cls.TR_THEME_KEY,
            cls.TR_THEME_ENDING_KEY,
            cls.S_THEME_KEY,
            cls.S_THEME_ENDING_KEY,
            cls.C_THEME_KEY,
            cls.C_THEME_ENDING_KEY
        }

    @classmethod
    def field_sql_type_list_pre_derived_fields(cls) -> List[Tuple[Field, SQLType]]:
        return [
            (cls.ID, SQLType.TEXT()),
            (cls.NUM_CYCLES, SQLType.INTEGER()),
            (cls.OPENING_TEMPO, SQLType.TEXT()),

            # P
            (cls.P_THEME_KEY, SQLType.TEXT()),
            (cls.P_THEME_DESCRIPTION, SQLType.TEXT()),
            (cls.P_THEME_CHANGE_FROM_EXPOSITION, SQLType.TEXT()),
            (cls.P_THEME_MOTIVES_LILYPOND, SQLType.JSONB()),  # If changed significantly
            (cls.P_THEME_ENDING_KEY, SQLType.TEXT()),
            (cls.P_THEME_ENDING_CADENCE, SQLType.TEXT()),

            # TR
            (cls.TR_THEME_PRESENT, SQLType.BOOLEAN()),
            (cls.TR_THEME_KEY, SQLType.TEXT()),
            (cls.TR_THEME_DESCRIPTION, SQLType.TEXT()),
            (cls.TR_THEME_CHANGE_FROM_EXPOSITION, SQLType.TEXT()),
            (cls.TR_THEME_MOTIVES_LILYPOND, SQLType.TEXT()),  # If changed significantly
            (cls.TR_THEME_ENDING_KEY, SQLType.TEXT()),
            (cls.TR_THEME_ENDING_CADENCE, SQLType.TEXT()),

            # MC
            (cls.MC_PRESENT, SQLType.BOOLEAN()),
            (cls.MC_CHANGE_FROM_EXPOSITION, SQLType.TEXT()),

            # S
            (cls.S_THEME_PRESENT, SQLType.TEXT()),
            (cls.S_THEME_KEY, SQLType.TEXT()),
            (cls.S_THEME_DESCRIPTION, SQLType.TEXT()),
            (cls.S_THEME_CHANGE_FROM_EXPOSITION, SQLType.TEXT()),
            (cls.S_THEME_MOTIVES_LILYPOND, SQLType.JSONB()),  # If changed significantly
            (cls.S_THEME_ENDING_KEY, SQLType.TEXT()),
            (cls.S_THEME_ENDING_CADENCE, SQLType.TEXT()),

            # EEC
            (cls.ESC_PRESENT, SQLType.BOOLEAN()),
            (cls.ESC_FAKED_OUT_COUNT, SQLType.INTEGER()),
            (cls.ESC_STRENGTH, SQLType.TEXT()),
            (cls.ESC_CHANGE_FROM_EXPOSITION, SQLType.TEXT()),

            # C
            (cls.C_THEME_PRESENT, SQLType.BOOLEAN()),
            (cls.C_THEME_KEY, SQLType.TEXT()),
            (cls.C_THEME_DESCRIPTION, SQLType.TEXT()),
            (cls.C_THEME_MOTIVES_LILYPOND, SQLType.JSONB()),  # If changed significantly
            (cls.C_THEME_CHANGE_FROM_EXPOSITION, SQLType.TEXT()),
            (cls.C_THEME_ENDING_KEY, SQLType.TEXT()),
        ]

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

    NUM_CYCLES = Field("num_cycles")

    INTRODUCTION_TYPE = Field("coda_type")
    OPENING_KEY = Field("opening_key")
    OPENING_TEMPO = Field("opening_tempo")
    KEYS_TONICIZED = Field("keys_tonicized")  # a JSONArray of keys tonicized
    P_THEME_RECALLED = Field("p_theme_recalled")
    TR_THEME_RECALLED = Field("tr_theme_recalled")
    S_THEME_RECALLED = Field("s_theme_recalled")
    C_THEME_RECALLED = Field("c_theme_recalled")

    # Coda Theme
    CODA_THEME_PRESENT = Field("coda_theme_present")  # whether the coda contains a novel theme
    CODA_THEME_KEY = Field("coda_theme_key")
    CODA_THEME_DESCRIPTION = Field("coda_theme_description")
    CODA_THEME_MOTIVES_LILYPOND = Field("coda_theme_motives_lilypond")

    ENDING_KEY = Field("ending_key")
    ENDING_CADENCE = Field("ending_cadence")

    @classmethod
    def absolute_key_fields(cls) -> Set[Field]:
        return {
            cls.OPENING_KEY,
            cls.CODA_THEME_KEY,
            cls.ENDING_KEY,
        }

    @classmethod
    def field_sql_type_list_pre_derived_fields(cls) -> List[Tuple[Field, SQLType]]:
        return [
            (cls.ID, SQLType.TEXT()),
            (cls.NUM_CYCLES, SQLType.INTEGER()),

            (cls.INTRODUCTION_TYPE, SQLType.TEXT()),
            (cls.OPENING_KEY, SQLType.TEXT()),
            (cls.OPENING_TEMPO, SQLType.TEXT()),
            (cls.KEYS_TONICIZED, SQLType.JSONB()),  # JSONArray
            (cls.P_THEME_RECALLED, SQLType.BOOLEAN()),
            (cls.TR_THEME_RECALLED, SQLType.BOOLEAN()),
            (cls.S_THEME_RECALLED, SQLType.BOOLEAN()),
            (cls.C_THEME_RECALLED, SQLType.BOOLEAN()),

            # Coda Theme
            (cls.CODA_THEME_PRESENT, SQLType.BOOLEAN()),
            (cls.CODA_THEME_KEY, SQLType.TEXT()),
            (cls.CODA_THEME_DESCRIPTION, SQLType.TEXT()),
            (cls.CODA_THEME_MOTIVES_LILYPOND, SQLType.JSONB()),

            (cls.ENDING_KEY, SQLType.TEXT()),
            (cls.ENDING_CADENCE, SQLType.TEXT()),
        ]

    @classmethod
    def create_constraints_sql(cls) -> sql.Composable:
        return sql.SQL("ALTER TABLE {st} ADD PRIMARY KEY ({id});").format(st=cls.schema_table(), id=cls.ID)
