#!/usr/bin/env python
"""
A module containing the abstract base classes that all sonata_data classes will extend
"""
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any

from psycopg2 import sql

from database_design.sonata_table_specs import Composer, Piece, Sonata, Introduction, Exposition, Development, \
    Recapitulation, Coda
from general_utils.postgres_utils import LocalhostCursor
from general_utils.sql_utils import Field, upsert_sql_from_field_value_dict

log = logging.getLogger(__name__)


class ComposerDataClass(ABC):
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
    def upsert_data(cls) -> None:
        """
        The core upsert method that uses the attribute dict to insert (if the relevant id does not exist) or update (
        if the id does exist).
        """

        with LocalhostCursor() as cur:
            # Use postgres's brand-new ON CONFLICT framework that allows for upserting
            # EXCLUDED is the posgres name of the records that couldn't be inserted so we use update with those records

            # Upsert Composer
            upsert_sql = upsert_sql_from_field_value_dict(Composer.schema_table(), cls.composer_attribute_dict(),
                                                          conflict_field_list=[Composer.ID])
            log.info("\n\n" + upsert_sql.as_string(cur) + "\n")
            cur.execute(upsert_sql)


class PieceDataClass(ABC):
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
    def upsert_data(cls) -> None:
        """
        The core upsert method that uses the attribute dict to insert (if the relevant id does not exist) or update (
        if the id does exist).
        """

        with LocalhostCursor() as cur:
            # Use postgres's brand-new ON CONFLICT framework that allows for upserting
            # EXCLUDED is the posgres name of the records that couldn't be inserted so we use update with those records

            # Upsert Piece
            upsert_sql = upsert_sql_from_field_value_dict(Piece.schema_table(), cls.piece_attribute_dict(),
                                                          conflict_field_list=[Piece.ID])
            log.info("\n\n" + upsert_sql.as_string(cur) + "\n")
            cur.execute(upsert_sql)


class SonataDataClass(ABC):
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
    @abstractmethod
    def sonata_attribute_dict(cls) -> Dict[Field, Any]:
        """
        An abstract method that each subclass must implement that contains a dictionary mapping attributes from
        the Piece table spec to their values.

        Must ALWAYS specify the piece id, the movement_num and the booleans for whether the introduction, development or coda
        are present.

        Do not need to add the id column or the links to the 5 blocks as they are handled automatically.

        :return: a dict of fields to their values
        """

    @classmethod
    def introduction_attribute_dict(cls) -> Dict[Field, Any]:
        """
        A method that contains a dictionary mapping attributes from the Coda table spec to their values. Not abstract
        because not all sonatas have an Introduction, but if you choose True for development_present, you must include
        this.

        Do not need to add the id column as it is handled automatically.

        :return: a dict of fields to their values
        """
        raise NotImplementedError("Must implement in the subclass since you chose introduction_present = True")

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
        this.

        Do not need to add the id column as it is handled automatically.

        :return: a dict of fields to their values
        """
        raise NotImplementedError("Must implement in the subclass since you chose development_present = True")

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
        because not all sonatas have a Coda, but if you choose True for coda_present, you must include this.

        Do not need to add the id column as it is handled automatically.

        :return: a dict of fields to their values
        """
        raise NotImplementedError("Must implement in the subclass since you chose coda_present = True")

    @classmethod
    def upsert_data(cls) -> None:
        """
        The core upsert method that uses the attribute dicts to insert (if the relevant ids do not exist) or update
        the tables ( if the id does exist)

        Simultaneously updates both the sonata object and anywhere from the 2 essential to the 5 sonata blocks depending
        on the presence of the booleans for which blocks are present
        """

        with LocalhostCursor() as cur:

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
            block_dict = cls.exposition_attribute_dict()
            block_dict[Exposition.ID] = expo_id
            sonata_dict[Sonata.EXPOSITION_ID] = expo_id
            upsert_sql = upsert_sql_from_field_value_dict(Exposition.schema_table(), block_dict,
                                                          conflict_field_list=[Exposition.ID])
            log.info(upsert_sql.as_string(cur) + "\n")
            cur.execute(upsert_sql)

            # Upsert Recapitulation
            block_dict = cls.recapitulation_attribute_dict()
            block_dict[Recapitulation.ID] = recap_id
            sonata_dict[Sonata.RECAPITULATION_ID] = recap_id
            upsert_sql = upsert_sql_from_field_value_dict(Recapitulation.schema_table(), block_dict,
                                                          conflict_field_list=[Recapitulation.ID])
            log.info(upsert_sql.as_string(cur) + "\n")
            cur.execute(upsert_sql)

            # Upsert the 3 optional sonata block tables that they will have depending on the booleans present

            # Upsert Introduction if boolean True
            if cls.sonata_attribute_dict()[Sonata.INTRODUCTION_PRESENT]:
                block_dict = cls.introduction_attribute_dict()
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
                block_dict = cls.development_attribute_dict()
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

            # Upsert Coda if boolean
            if cls.sonata_attribute_dict()[Sonata.CODA_PRESENT]:
                block_dict = cls.coda_attribute_dict()
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
