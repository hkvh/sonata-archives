#!/usr/bin/env python
import logging
from typing import Dict, Any

from datetime import date
from data.composers import Beethoven
from database_design.sonata_data_classes import PieceDataClass, SonataDataClass
from database_design.sonata_enums import PieceType, SonataType
from database_design.sonata_table_specs import Piece, Sonata, Exposition, Development, Recapitulation
from general_utils.sql_utils import Field


class Beethoven5(PieceDataClass):
    @classmethod
    def piece_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Piece.ID:             "beethoven5",
            Piece.COMPOSER_ID:    Beethoven.id(),
            Piece.NAME:           "Symphony No. 5",
            Piece.CATALOGUE_ID:   "Op. 67",
            Piece.GLOBAL_KEY:     "C Minor",
            Piece.PREMIER_DATE:   date(1808, 12, 22),
            Piece.YEAR_STARTED:   1804,
            Piece.YEAR_COMPLETED: 1808,
            Piece.NUM_MOVEMENTS:  4,
            Piece.PIECE_TYPE:     PieceType.SYMPHONY()
        }


class Beethoven5_1(SonataDataClass):

    @classmethod
    def sonata_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Sonata.ID:                       Beethoven5.id() + "_1",
            Sonata.PIECE_ID:                 Beethoven5.id(),
            Sonata.SONATA_TYPE:              SonataType.TYPE_3(),
            Sonata.INTRODUCTION_PRESENT:     False,
            Sonata.DEVELOPMENT_PRESENT:      True,
            Sonata.CODA_PRESENT:             True,
            Sonata.MOVEMENT_NUM:             1,
            Sonata.EXPOSITION_REPEAT:        True,
            Sonata.DEVELOPMENT_RECAP_REPEAT: False,
        }

    @classmethod
    def exposition_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Exposition.OPENING_TEMPO: "Allegro con brio",
            Exposition.P_THEME_KEY:   "C minor",
            Exposition.S_THEME_KEY:   "E♭ Major",
            Exposition.EEC_PRESENT:   True
        }

    @classmethod
    def recapitulation_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Recapitulation.OPENING_TEMPO: "Allegro con brio",
            Recapitulation.P_THEME_KEY:   "C minor",
            Recapitulation.S_THEME_KEY:   "C Major",
            Recapitulation.ESC_PRESENT:   True,
        }

    @classmethod
    def development_attribute_dict(cls) -> Dict[Field, Any]:
        return {

        }

    @classmethod
    def coda_attribute_dict(cls) -> Dict[Field, Any]:
        return {

        }


class Beethoven5_4(SonataDataClass):
    @classmethod
    def sonata_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Sonata.ID:                       Beethoven5.id() + "_4",
            Sonata.PIECE_ID:                 Beethoven5.id(),
            Sonata.SONATA_TYPE:              SonataType.TYPE_3(),
            Sonata.INTRODUCTION_PRESENT:     False,
            Sonata.DEVELOPMENT_PRESENT:      True,
            Sonata.CODA_PRESENT:             True,
            Sonata.MOVEMENT_NUM:             4,
            Sonata.EXPOSITION_REPEAT:        True,
            Sonata.DEVELOPMENT_RECAP_REPEAT: False,
        }

    @classmethod
    def exposition_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Exposition.OPENING_TEMPO:   "Allegro",
            Exposition.P_THEME_KEY:     "C Major",
            Exposition.S_THEME_PRESENT: True,
            Exposition.S_THEME_KEY:     "G Major",
            Exposition.C_THEME_PRESENT: True,
            Exposition.EEC_PRESENT:     True
        }

    @classmethod
    def recapitulation_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Recapitulation.OPENING_TEMPO: "Allegro",
            Recapitulation.P_THEME_KEY:   "C Major",
            Recapitulation.S_THEME_KEY:   "C Major",
            Recapitulation.ESC_PRESENT:   True,
        }

    @classmethod
    def development_attribute_dict(cls) -> Dict[Field, Any]:
        return {

        }

    @classmethod
    def coda_attribute_dict(cls) -> Dict[Field, Any]:
        return {

        }


# Upsert everything into the database
def upsert_all():
    for x in [Beethoven5, Beethoven5_1, Beethoven5_4]:
        x.upsert_data()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)s %(levelname)s: %(message)s')
    upsert_all()
