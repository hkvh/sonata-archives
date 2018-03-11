#!/usr/bin/env python
import typing
from datetime import date
from typing import Dict, Any

from data.composers import Beethoven
from database_design.key_enums import Key
from database_design.sonata_data_classes import PieceDataClass, SonataDataClass
from database_design.sonata_enums import PieceType, SonataType
from database_design.sonata_table_specs import Piece, Sonata, Exposition, Recapitulation, Development
from general_utils.sql_utils import Field


#################
# Piece
#################

class Beethoven5(PieceDataClass):
    @classmethod
    def piece_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Piece.ID:             "beethoven5",
            Piece.COMPOSER_ID:    Beethoven.id(),
            Piece.NAME:           "Symphony No. 5",
            Piece.CATALOGUE_ID:   "Op. 67",
            Piece.GLOBAL_KEY:     Key.C_MINOR,
            Piece.PREMIER_DATE:   date(1808, 12, 22),
            Piece.YEAR_STARTED:   1804,
            Piece.YEAR_COMPLETED: 1808,
            Piece.NUM_MOVEMENTS:  4,
            Piece.PIECE_TYPE:     PieceType.SYMPHONY
        }


#################
# Sonata(s)
#################

class Beethoven5_1(SonataDataClass):
    @classmethod
    def sonata_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Sonata.PIECE_ID:                 Beethoven5.id(),
            Sonata.MOVEMENT_NUM:             1,
            Sonata.SONATA_TYPE:              SonataType.TYPE_3,
            Sonata.GLOBAL_KEY:               Key.C_MINOR,
            Sonata.INTRODUCTION_PRESENT:     False,
            Sonata.DEVELOPMENT_PRESENT:      True,
            Sonata.CODA_PRESENT:             True,
            Sonata.EXPOSITION_REPEAT:        True,
            Sonata.DEVELOPMENT_RECAP_REPEAT: False,
        }

    @classmethod
    def exposition_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Exposition.OPENING_TEMPO:   "Allegro con brio",
            Exposition.P_THEME_KEY:     Key.C_MINOR,
            Exposition.S_THEME_PRESENT: True,
            Exposition.S_THEME_KEY:     Key.E_FLAT_MAJOR,
            Exposition.EEC_PRESENT:     True
        }

    @classmethod
    def development_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Development.OPENING_KEY: Key.F_MINOR,
            Development.KEYS_TONICIZED: [
                Key.F_MINOR,
                Key.C_MINOR,
                Key.G_MINOR,
                Key.C_MINOR,
                Key.F_MINOR,
                Key.C_MINOR,
            ]

        }

    @classmethod
    def recapitulation_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Recapitulation.OPENING_TEMPO: "Allegro con brio",
            Recapitulation.P_THEME_KEY:   Key.C_MINOR,
            Recapitulation.S_THEME_KEY:   Key.C_MAJOR,
            Recapitulation.ESC_PRESENT:   True,
        }

    @classmethod
    def coda_attribute_dict(cls) -> Dict[Field, Any]:
        return {

        }


class Beethoven5_4(SonataDataClass):
    @classmethod
    def sonata_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Sonata.PIECE_ID:                 Beethoven5.id(),
            Sonata.MOVEMENT_NUM:             4,
            Sonata.SONATA_TYPE:              SonataType.TYPE_3,
            Sonata.GLOBAL_KEY:               Key.C_MAJOR,
            Sonata.INTRODUCTION_PRESENT:     False,
            Sonata.DEVELOPMENT_PRESENT:      True,
            Sonata.CODA_PRESENT:             True,
            Sonata.EXPOSITION_REPEAT:        True,
            Sonata.DEVELOPMENT_RECAP_REPEAT: False,
        }

    @classmethod
    def exposition_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Exposition.OPENING_TEMPO:   "Allegro",
            Exposition.P_THEME_KEY:     Key.C_MAJOR,
            Exposition.S_THEME_PRESENT: True,
            Exposition.S_THEME_KEY:     Key.G_MAJOR,
            Exposition.C_THEME_PRESENT: True,
            Exposition.EEC_PRESENT:     True
        }

    @classmethod
    def development_attribute_dict(cls) -> Dict[Field, Any]:
        return {

        }

    @classmethod
    def recapitulation_attribute_dict(cls) -> typing.Mapping[str, str]:
        return {
            Recapitulation.OPENING_TEMPO: "Allegro",
            Recapitulation.P_THEME_KEY:   Key.C_MAJOR,
            Recapitulation.S_THEME_KEY:   Key.C_MAJOR,
            Recapitulation.ESC_PRESENT:   True,
        }

    @classmethod
    def coda_attribute_dict(cls) -> Dict[Field, Any]:
        return {

        }
