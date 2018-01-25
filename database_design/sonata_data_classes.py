#!/usr/bin/env python
"""
A module containing the abstract base classes that data classes will extend
"""
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any

from psycopg2 import sql

from database_design.sonata_table_specs import Composer, Piece, Sonata, Introduction, Exposition, Development, \
    Recapitulation, Coda
from general_utils.postgres_utils import LocalhostCursor
from general_utils.sql_utils import Field

log = logging.getLogger(__name__)

upsert_sql_str = sql.SQL("INSERT INTO {st} ({field_list}) VALUES ({val_list}) \n"
                         "ON CONFLICT ({id}) \n"
                         " DO UPDATE SET ({field_list}) = ({excluded_field_list})")


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
            upsert_sql = upsert_sql_str.format(st=Composer.schema_table(),
                                               field_list=sql.SQL(", ").join(cls.composer_attribute_dict().keys()),
                                               excluded_field_list=sql.SQL(", ").join(
                                                   [sql.SQL("EXCLUDED.{}").format(x)
                                                    for x in cls.composer_attribute_dict().keys()]),
                                               val_list=sql.SQL(", ").join([sql.Literal(x) for x in
                                                                            cls.composer_attribute_dict().values()]),
                                               id=Composer.ID)
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
            upsert_sql = upsert_sql_str.format(st=Piece.schema_table(),
                                               field_list=sql.SQL(", ").join(cls.piece_attribute_dict().keys()),
                                               excluded_field_list=sql.SQL(", ").join(
                                                   [sql.SQL("EXCLUDED.{}").format(x)
                                                    for x in cls.piece_attribute_dict().keys()]),
                                               val_list=sql.SQL(", ").join(
                                                   [sql.Literal(x) for x in cls.piece_attribute_dict().values()]),
                                               id=Piece.ID)
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
        Returns the id column for the piece by grabbing the appropriate column from its piece_attribute_dict
        :return: the id of this Piece
        """
        return cls.sonata_attribute_dict()[Sonata.ID]

    @classmethod
    @abstractmethod
    def sonata_attribute_dict(cls) -> Dict[Field, Any]:
        """
        An abstract method that each subclass must implement that contains a dictionary mapping attributes from
        the Piece table spec to their values.

        Must specify at least the id, the piece id and the booleans for whether the introduction, development or coda
        are present.

        Do not need to add the foreign keys for introduction, development or coda if the aforementioned booleans are
        false.

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

            # Use postgres's brand-new ON CONFLICT framework that allows for upserting
            # EXCLUDED is the posgres name of the records that couldn't be inserted so we use update with those records

            # Upsert Sonata
            upsert_sql = upsert_sql_str.format(st=Sonata.schema_table(),
                                               field_list=sql.SQL(", ").join(cls.sonata_attribute_dict().keys()),
                                               excluded_field_list=sql.SQL(", ").join(
                                                   [sql.SQL("EXCLUDED.{}").format(x)
                                                    for x in cls.sonata_attribute_dict().keys()]),
                                               val_list=sql.SQL(", ").join(
                                                   [sql.Literal(x) for x in cls.sonata_attribute_dict().values()]),
                                               id=Sonata.ID)
            log.info("\n\n" + upsert_sql.as_string(cur) + "\n")
            cur.execute(upsert_sql)

            # Will auto-add ids for each of the 5 sonata blocks by appending i/e/d/r/c
            intro_id = cls.id() + "_i"
            expo_id = cls.id() + "_e"
            devel_id = cls.id() + "_d"
            recap_id = cls.id() + "_r"
            coda_id = cls.id() + "_c"

            # Upsert the 2 essential sonata block tables that all sonatas have

            # Upsert Exposition
            block_dict = cls.exposition_attribute_dict()
            block_dict[Exposition.ID] = expo_id
            upsert_sql = upsert_sql_str.format(st=Exposition.schema_table(),
                                               field_list=sql.SQL(", ").join(block_dict.keys()),
                                               excluded_field_list=sql.SQL(", ").join(
                                                   [sql.SQL("EXCLUDED.{}").format(x) for x in block_dict.keys()]),
                                               val_list=sql.SQL(", ").join(
                                                   [sql.Literal(x) for x in block_dict.values()]),
                                               id=Exposition.ID)
            log.info("\n\n" + upsert_sql.as_string(cur) + "\n")
            cur.execute(upsert_sql)

            # Upsert Recapitulation
            block_dict = cls.recapitulation_attribute_dict()
            block_dict[Recapitulation.ID] = recap_id
            upsert_sql = upsert_sql_str.format(st=Recapitulation.schema_table(),
                                               field_list=sql.SQL(", ").join(block_dict.keys()),
                                               excluded_field_list=sql.SQL(", ").join(
                                                   [sql.SQL("EXCLUDED.{}").format(x) for x in block_dict.keys()]),
                                               val_list=sql.SQL(", ").join(
                                                   [sql.Literal(x) for x in block_dict.values()]),
                                               id=Recapitulation.ID)
            log.info("\n\n" + upsert_sql.as_string(cur) + "\n")
            cur.execute(upsert_sql)

            # Upsert the 3 optional sonata block tables that they will have depending on the booleans present

            # Upsert Introduction if boolean
            if cls.sonata_attribute_dict()[Sonata.INTRODUCTION_PRESENT]:
                block_dict = cls.introduction_attribute_dict()
                block_dict[Introduction.ID] = intro_id
                upsert_sql = upsert_sql_str.format(st=Introduction.schema_table(),
                                                   field_list=sql.SQL(", ").join(block_dict.keys()),
                                                   excluded_field_list=sql.SQL(", ").join(
                                                       [sql.SQL("EXCLUDED.{}").format(x) for x in block_dict.keys()]),
                                                   val_list=sql.SQL(", ").join(
                                                       [sql.Literal(x) for x in block_dict.values()]),
                                                   id=Introduction.ID)
                log.info("\n\n" + upsert_sql.as_string(cur) + "\n")
                cur.execute(upsert_sql)

            # Upsert Development if boolean
            if cls.sonata_attribute_dict()[Sonata.DEVELOPMENT_PRESENT]:
                block_dict = cls.development_attribute_dict()
                block_dict[Development.ID] = devel_id
                upsert_sql = upsert_sql_str.format(st=Development.schema_table(),
                                                   field_list=sql.SQL(", ").join(block_dict.keys()),
                                                   excluded_field_list=sql.SQL(", ").join(
                                                       [sql.SQL("EXCLUDED.{}").format(x) for x in block_dict.keys()]),
                                                   val_list=sql.SQL(", ").join(
                                                       [sql.Literal(x) for x in block_dict.values()]),
                                                   id=Development.ID)
                log.info("\n\n" + upsert_sql.as_string(cur) + "\n")
                cur.execute(upsert_sql)

            # Upsert Coda if boolean
            if cls.sonata_attribute_dict()[Sonata.CODA_PRESENT]:
                block_dict = cls.coda_attribute_dict()
                block_dict[Coda.ID] = coda_id
                upsert_sql = upsert_sql_str.format(st=Coda.schema_table(),
                                                   field_list=sql.SQL(", ").join(block_dict.keys()),
                                                   excluded_field_list=sql.SQL(", ").join(
                                                       [sql.SQL("EXCLUDED.{}").format(x) for x in block_dict.keys()]),
                                                   val_list=sql.SQL(", ").join(
                                                       [sql.Literal(x) for x in block_dict.values()]),
                                                   id=Coda.ID)
                log.info("\n\n" + upsert_sql.as_string(cur) + "\n")
                cur.execute(upsert_sql)
