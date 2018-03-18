#!/usr/bin/env python
"""
A module containing the abstract base classes that all sonata_data classes will extend
"""
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Type, Union

from psycopg2 import sql, extensions

from enums.key_enums import KeyStruct, validate_is_key_struct
from database_design.sonata_table_specs import Composer, Piece, Sonata, Introduction, Exposition, Development, \
    Recapitulation, Coda, SonataBlockTableSpecification
from enums.measure_enums import validate_is_measure_range
from general_utils.sql_utils import Field, upsert_sql_from_field_value_dict

log = logging.getLogger(__name__)


class DataClass(ABC):
    """
    An abstract base class that all Data Classes will extend an implement its upsert_data method.
    """

    @classmethod
    @abstractmethod
    def upsert_data(cls, cur: extensions.cursor) -> None:
        """
        The core upsert method that the data class must implement to describe how to write itself to the postgres db

        :param cur: the postgres cursor to use to upsert the data
        """


class ComposerDataClass(DataClass, ABC):
    """
    An abstract base class whose subclasses will store data about a composer.

    These objects are not meant to be instantiated - simply use their class methods and properties.
    """

    @classmethod
    def id(cls) -> str:
        """
        Returns the id column for the piece by grabbing the appropriate column from its piece_attribute_dict
        :return: the id of this Piece
        """
        return cls.composer_attribute_dict()[Composer.ID]

    @classmethod
    @abstractmethod
    def composer_attribute_dict(cls) -> Dict[Field, Any]:
        """
        An abstract method that each subclass must implement that contains a dictionary mapping attributes from
        the Composer table spec to their values

        Must specify at least the id.

        :return: a dict of field to their values
        """

    @classmethod
    def upsert_data(cls, cur: extensions.cursor) -> None:
        """
        The core upsert method that uses the attribute dict to insert (if the relevant id does not exist) or update (
        if the id does exist).

        :param cur: the postgres cursor to use to upsert the data
        """

        # Use postgres's brand-new ON CONFLICT framework that allows for upserting
        # EXCLUDED is the posgres name of the records that couldn't be inserted so we use update with those records

        # Upsert Composer
        upsert_sql = upsert_sql_from_field_value_dict(Composer.schema_table(), cls.composer_attribute_dict(),
                                                      conflict_field_list=[Composer.ID])
        log.info("\n\n" + upsert_sql.as_string(cur) + "\n")
        cur.execute(upsert_sql)


class PieceDataClass(DataClass, ABC):
    """
    An abstract base class whose subclasses will store data about a piece.

    These objects are not meant to be instantiated - simply use their class methods and properties.
    """

    @classmethod
    def id(cls) -> str:
        """
        Returns the id column for the piece by grabbing the appropriate column from its piece_attribute_dict
        :return: the id of this Piece
        """
        return cls.piece_attribute_dict()[Piece.ID]

    @classmethod
    @abstractmethod
    def piece_attribute_dict(cls) -> Dict[Field, Any]:
        """
        An abstract method that each subclass must implement that contains a dictionary mapping attributes from
        the Piece table spec to their values,

        Must specify at least the id and the composer id.

        :return: a dict of fields to their values
        """

    @classmethod
    def upsert_data(cls, cur) -> None:
        """
        The core upsert method that uses the attribute dict to insert (if the relevant id does not exist) or update (
        if the id does exist).

        If no full name was provided for the Piece, it will create it based on its name, catalogue_id and nickname.

        :param cur: the postgres cursor to use to upsert the data
        """
        piece_dict = cls.piece_attribute_dict()

        if Piece.FULL_NAME not in piece_dict:
            piece_dict[Piece.FULL_NAME] = cls.create_full_name(name=piece_dict.get(Piece.NAME),
                                                               catalogue_id=piece_dict.get(Piece.CATALOGUE_ID),
                                                               nickname=piece_dict.get(Piece.NICKNAME),
                                                               global_key=piece_dict.get(Piece.GLOBAL_KEY))
            # Note: using .get() instead of [] so no key error if not there

        # Use postgres's brand-new ON CONFLICT framework that allows for upserting
        # EXCLUDED is the posgres name of the records that couldn't be inserted so we use update with those records

        # Upsert Piece
        upsert_sql = upsert_sql_from_field_value_dict(Piece.schema_table(), piece_dict,
                                                      conflict_field_list=[Piece.ID])
        log.info("\n\n" + upsert_sql.as_string(cur) + "\n")
        cur.execute(upsert_sql)

    @classmethod
    def create_full_name(cls, name: str, catalogue_id: Union[str, None] = None, nickname: Union[str, None] = None,
                         global_key: Union[KeyStruct, None] = None):
        """
        Given the name, catalogue_id, nickname and global key, creates the full name for the piece

        :param name: the str name of the piece, like Symphony No. 5 (required)
        :param catalogue_id: the str catalogue id, like Opus No. (optional)
        :param nickname: the str nickname (optional)
        :param global_key: the global key of the piece, stored in a KeyStruct (optional)
        :return: a string like <piece_name> "<nickname>", <catalogue_id> or parts of this if the latter two are blank.
        Will raise an exception if all name is blank or None, or if global key was not a KeyStruct
        """

        if name is None or name == "":
            raise Exception("The piece must have a name and it was left blank or None")

        full_name = name
        if global_key is not None:
            validate_is_key_struct(global_key)
            full_name = "{} in {}".format(full_name, global_key.key_name_with_major_implied)

        if catalogue_id is not None:
            full_name = "{}, {}".format(full_name, catalogue_id)

        if nickname is not None:
            full_name = "{} \"{}\"".format(full_name, nickname)

        return full_name


class SonataDataClass(DataClass, ABC):
    """
    An abstract base class whose subclasses will store data about a sonata.

    These objects are not meant to be instantiated - simply use their class methods and properties.
    """

    @classmethod
    def id(cls) -> str:
        """
        Returns the id column for the sonata by appending the provided movement_num onto the piece_id
        :return: the id of this Sonata
        """
        return "{}_{}".format(cls.sonata_attribute_dict()[Sonata.PIECE_ID],
                              cls.sonata_attribute_dict()[Sonata.MOVEMENT_NUM])

    @classmethod
    def global_key(cls) -> KeyStruct:
        """
        Returns the global key for this sonata for use in computing relative keys.

        :return: the global key of this sonata (or KeyError if you forgot to enter the global key was not entered)
        """
        try:
            global_key = cls.sonata_attribute_dict()[Sonata.GLOBAL_KEY]
            validate_is_key_struct(global_key)
            return global_key
        except KeyError:
            raise KeyError("You forgot to enter the global_key for sonata {}!".format(cls.id()))
        except TypeError:
            raise TypeError("You did not enter the global_key for sonata {} as a KeyStruct!".format(cls.id()))

    @classmethod
    @abstractmethod
    def sonata_attribute_dict(cls) -> Dict[Field, Any]:
        """
        An abstract method that each subclass must implement that contains a dictionary mapping attributes from
        the Piece table spec to their values.

        Must ALWAYS specify the piece id, the movement_num and the booleans for whether the introduction, development
        or coda are present.

        Do not need to add the id column or the links to the 5 blocks as they are handled automatically.

        :return: a dict of fields to their values
        """

    @classmethod
    def introduction_attribute_dict(cls) -> Dict[Field, Any]:
        """
        A method that contains a dictionary mapping attributes from the Coda table spec to their values. Not abstract
        because not all sonatas have an Introduction, but if you choose True for development_present, you must include
        this unless you want it to be blank

        Do not need to add the id column as it is handled automatically.

        :return: a dict of fields to their values
        """
        return {

        }

    @classmethod
    @abstractmethod
    def exposition_attribute_dict(cls) -> Dict[Field, Any]:
        """
        An abstract method that each subclass must implement that contains a dictionary mapping attributes from
        the Exposition table spec to their values

        Do not need to add the id column as it is handled automatically.

        :return: a dict of fields to their values
        """

    @classmethod
    def development_attribute_dict(cls) -> Dict[Field, Any]:
        """
        A method that contains a dictionary mapping attributes from the Coda table spec to their values. Not abstract
        because not all sonatas have a Development, but if you choose True for development_present, you must include
        this unless you want it to be blank.

        Do not need to add the id column as it is handled automatically.

        :return: a dict of fields to their values
        """
        return {

        }

    @classmethod
    @abstractmethod
    def recapitulation_attribute_dict(cls) -> Dict[Field, Any]:
        """
        An abstract method that each subclass must implement that contains a dictionary mapping attributes from
        the Recapitulation table spec to their values

        Do not need to add the id column as it is handled automatically.

        :return: a dict of fields to their values
        """

    @classmethod
    def coda_attribute_dict(cls) -> Dict[Field, Any]:
        """
        A method that contains a dictionary mapping attributes from the Coda table spec to their values. Not abstract
        because not all sonatas have a Coda, but if you choose True for coda_present, you must include this unless
        you want it to be blank.

        Do not need to add the id column as it is handled automatically.

        :return: a dict of fields to their values
        """
        return {

        }

    @classmethod
    def _convert_absolute_to_relative(cls, obj):
        """
        Recursive helper method that traverses a scalar, dict or list object (or any composition of them) and
        converts all KeyStruct values it finds to the relative key. Assumes that all non-dict keys in the nested
        structure were KeyStruct instances

        :param obj: the scalar KeyStruct, dict or list to operate on
        :return: the object converted
        :raises TypeError if any of the values of the dict / list were NOT KeyStructs
        """
        if isinstance(obj, list):
            new_obj = []
            for x in obj:
                new_obj.append(cls._convert_absolute_to_relative(x))
        elif isinstance(obj, dict):
            new_obj = {}
            for k, v in obj.items():
                new_obj[k] = cls._convert_absolute_to_relative(v)
        else:
            validate_is_key_struct(obj)  # Make sure any scalars are a key struct before trying to convert
            new_obj = obj.relative_key_wrt(cls.global_key())

        return new_obj

    @classmethod
    def _convert_measure_ranges_to_counts(cls, obj):
        """
        Recursive helper method that traverses a scalar, dict or list object (or any composition of them) and
        converts all measure ranges it finds to their counts. Assumes that all non-dict keys in the nested
        structure were MeasureRange instances.

        :param obj: the scalar KeyStruct, dict or list to operate on
        :return: the object converted
        :raises TypeError if any of the values of the dict / list were NOT MeasureRanges
        """
        if isinstance(obj, list):
            new_obj = []
            for x in obj:
                new_obj.append(cls._convert_measure_ranges_to_counts(x))
        elif isinstance(obj, dict):
            new_obj = {}
            for k, v in obj.items():
                new_obj[k] = cls._convert_measure_ranges_to_counts(v)
        else:
            validate_is_measure_range(obj)  # Make sure any scalars are a key struct before trying to convert
            new_obj = obj.count

        return new_obj

    @classmethod
    def augment_with_derived_fields(cls, attribute_dict: Dict[Field, Any],
                                    sonata_block_cls: Type[SonataBlockTableSpecification]) -> Dict[Field, Any]:
        """
        Takes an attribute_dict and a sonata block table spec subclass (the actual class name, not an instance since
        we never instantiate those classes) and augments it with derived fields that can be built through
        the sonata block table spec class.

        Right now the only derived fields we add are:

        1. Relative keys that correspond to absolute keys, so if any attribute dict specifies an absolute key we will
        dynamically detect that and derive its relative key and add it to the attribute dict to be inserted. (Will
        also detect Lists and Dicts and relativize everything inside them.)

        2. Measure Counts that correspond to measure ranges, so if any attribute dict specifies a measure range we
        will dynamically detect that and derive the counts and add it to the attribute dict to be inserted. (Will
        also detect Lists and Dicts and relativize everything inside them.)

        :param attribute_dict: the attribute dict to augment
        :param sonata_block_cls: the class of the sonata block that we will use to add the derived fields
        :return: a new attribute dict with the derived fields added
        """
        new_attribute_dict = {}
        for field, value in attribute_dict.items():
            new_attribute_dict[field] = value

            # If we added a field that we know contains an absolute key, compute and add its relative key counterpart
            if field in sonata_block_cls.absolute_key_fields():
                relative_key_field = sonata_block_cls.get_relative_from_absolute(field)
                new_attribute_dict[relative_key_field] = cls._convert_absolute_to_relative(value)

            if field in sonata_block_cls.measure_range_fields():
                measure_count_field = sonata_block_cls.get_measure_count_from_measure_range(field)
                new_attribute_dict[measure_count_field] = cls._convert_measure_ranges_to_counts(value)

        return new_attribute_dict

    @classmethod
    def upsert_data(cls, cur: extensions.cursor) -> None:
        """
        The core upsert method that uses the attribute dicts to insert (if the relevant ids do not exist) or update
        the tables ( if the id does exist)

        Simultaneously updates both the sonata object and anywhere from the 2 essential to the 5 sonata blocks depending
        on the presence of the booleans for which blocks are present

        :param cur: the postgres cursor to use to upsert the data
        """

        # Will auto-add ids for each of the 5 sonata blocks by appending i/e/d/r/c
        intro_id = "{}_i".format(cls.id())
        expo_id = "{}_e".format(cls.id())
        devel_id = "{}_d".format(cls.id())
        recap_id = "{}_r".format(cls.id())
        coda_id = "{}_c".format(cls.id())

        # Will be add these ids to the sonata dict if the booleans imply we should
        sonata_dict = cls.sonata_attribute_dict()

        #################
        # SONATA BLOCKS
        ################
        # Upsert the 2 essential sonata block tables that all sonatas have

        # Upsert Exposition
        block_dict = cls.augment_with_derived_fields(cls.exposition_attribute_dict(), Exposition)
        block_dict[Exposition.ID] = expo_id
        sonata_dict[Sonata.EXPOSITION_ID] = expo_id
        upsert_sql = upsert_sql_from_field_value_dict(Exposition.schema_table(), block_dict,
                                                      conflict_field_list=[Exposition.ID])
        log.info(upsert_sql.as_string(cur) + "\n")
        cur.execute(upsert_sql)

        # Upsert Recapitulation
        block_dict = cls.augment_with_derived_fields(cls.recapitulation_attribute_dict(), Recapitulation)
        block_dict[Recapitulation.ID] = recap_id
        sonata_dict[Sonata.RECAPITULATION_ID] = recap_id
        upsert_sql = upsert_sql_from_field_value_dict(Recapitulation.schema_table(), block_dict,
                                                      conflict_field_list=[Recapitulation.ID])
        log.info(upsert_sql.as_string(cur) + "\n")
        cur.execute(upsert_sql)

        # Upsert the 3 optional sonata block tables that they will have depending on the booleans present

        # Upsert Introduction if boolean True
        if cls.sonata_attribute_dict()[Sonata.INTRODUCTION_PRESENT]:
            block_dict = cls.augment_with_derived_fields(cls.introduction_attribute_dict(), Introduction)
            block_dict[Introduction.ID] = intro_id
            sonata_dict[Sonata.INTRODUCTION_ID] = intro_id
            upsert_sql = upsert_sql_from_field_value_dict(Introduction.schema_table(), block_dict,
                                                          conflict_field_list=[Introduction.ID])
            log.info(upsert_sql.as_string(cur) + "\n")
            cur.execute(upsert_sql)
        else:
            # Delete from Introduction if boolean false (this will cascade delete the sonata as well)
            delete_sql = sql.SQL("DELETE FROM {schema_table} WHERE {id} = {id_val};").format(
                schema_table=Introduction.schema_table(),
                id=Introduction.ID, id_val=sql.Literal(intro_id))
            log.info(delete_sql.as_string(cur) + "\n")
            cur.execute(delete_sql)

        # Upsert Development if boolean True
        if cls.sonata_attribute_dict()[Sonata.DEVELOPMENT_PRESENT]:
            block_dict = cls.augment_with_derived_fields(cls.development_attribute_dict(), Development)
            block_dict[Development.ID] = devel_id
            sonata_dict[Sonata.DEVELOPMENT_ID] = devel_id
            upsert_sql = upsert_sql_from_field_value_dict(Development.schema_table(), block_dict,
                                                          conflict_field_list=[Development.ID])
            log.info("\n\n" + upsert_sql.as_string(cur) + "\n")
            cur.execute(upsert_sql)
        else:
            # Delete from Development if boolean false (this will cascade delete the sonata as well)
            delete_sql = sql.SQL("DELETE FROM {schema_table} WHERE {id} = {id_val};").format(
                schema_table=Development.schema_table(),
                id=Development.ID, id_val=sql.Literal(devel_id))
            log.info(delete_sql.as_string(cur) + "\n")
            cur.execute(delete_sql)

        # Upsert Coda if boolean True
        if cls.sonata_attribute_dict()[Sonata.CODA_PRESENT]:
            block_dict = cls.augment_with_derived_fields(cls.coda_attribute_dict(), Coda)
            block_dict[Coda.ID] = coda_id
            sonata_dict[Sonata.CODA_ID] = coda_id
            upsert_sql = upsert_sql_from_field_value_dict(Coda.schema_table(), block_dict,
                                                          conflict_field_list=[Coda.ID])
            log.info(upsert_sql.as_string(cur) + "\n")
            cur.execute(upsert_sql)
        else:
            # Delete from Coda if boolean false (this will cascade delete the sonata as well)
            delete_sql = sql.SQL("DELETE FROM {schema_table} WHERE {id} = {id_val};").format(
                schema_table=Coda.schema_table(),
                id=Coda.ID, id_val=sql.Literal(coda_id))
            log.info(delete_sql.as_string(cur) + "\n")
            cur.execute(delete_sql)

        ###########
        # SONATA #
        ###########
        # Finally add the sonata's own id to the dict (since already added the rest)
        sonata_dict[Sonata.ID] = cls.id()

        # Upsert Sonata (with only links to the blocks we upserted)
        upsert_sql = upsert_sql_from_field_value_dict(Sonata.schema_table(), sonata_dict,
                                                      conflict_field_list=[Sonata.ID])

        # Note: because the FK constraints in the sonata table are cascade deletes, if any of the optional blocks
        # were true and the delete from actually deleted rows, the sonata will have been deleted as well
        # and this upsert is just an insert (so the link to the deleted block is wiped as well)
        log.info(upsert_sql.as_string(cur) + "\n")
        cur.execute(upsert_sql)
