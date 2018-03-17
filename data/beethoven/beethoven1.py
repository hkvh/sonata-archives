#!/usr/bin/env python
from datetime import date

from data.composers import Beethoven
from database_design.sonata_data_classes import PieceDataClass, SonataDataClass
from database_design.sonata_table_specs import *
from enums.key_enums import Key
from enums.sonata_enums import *
from general_utils.sql_utils import Field


#################
# Piece
#################

class Beethoven1(PieceDataClass):
    @classmethod
    def piece_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Piece.ID:             "beethoven1",
            Piece.COMPOSER_ID:    Beethoven.id(),
            Piece.NAME:           "Symphony No. 1",
            Piece.CATALOGUE_ID:   "Op. 21",
            Piece.GLOBAL_KEY:     Key.C_MAJOR,
            Piece.PREMIER_DATE:   date(1800, 4, 2),
            Piece.YEAR_STARTED:   1795,
            Piece.YEAR_COMPLETED: 1800,
            Piece.NUM_MOVEMENTS:  4,
            Piece.PIECE_TYPE:     PieceType.SYMPHONY
        }


#################
# Sonata(s)
#################

class Beethoven1_1(SonataDataClass):
    @classmethod
    def sonata_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Sonata.PIECE_ID:                 Beethoven1.id(),
            Sonata.MOVEMENT_NUM:             1,
            Sonata.SONATA_TYPE:              SonataType.TYPE_3,
            Sonata.GLOBAL_KEY:               Key.C_MAJOR,
            Sonata.INTRODUCTION_PRESENT:     True,
            Sonata.DEVELOPMENT_PRESENT:      True,
            Sonata.CODA_PRESENT:             True,
            Sonata.EXPOSITION_REPEAT:        True,
            Sonata.DEVELOPMENT_RECAP_REPEAT: False,

            # Delete this attribute if did not render a lilypond image for this sonata
            # Sonata.LILYPOND_IMAGE_SETTINGS:  {Sonata.IMAGE_WIDTH: 460}
        }

    @classmethod
    def introduction_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Introduction.MEASURES:      measure_number_range(1, 12),
            Introduction.OPENING_TEMPO: "Adagio molto",
            Introduction.OPENING_KEY:   Key.F_MAJOR,
            Introduction.ENDING_KEY:    Key.C_MAJOR,
        }

    @classmethod
    def exposition_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Exposition.MEASURES:                       measure_number_range(13, 109),

            Exposition.P_THEME_MEASURES:               measure_number_range(13, 33),
            Exposition.P_THEME_KEY:                    Key.C_MAJOR,

            Exposition.TR_THEME_MEASURES:              measure_number_range(33, 52),
            Exposition.TR_THEME_OPENING_KEY:           Key.C_MAJOR,
            Exposition.TR_THEME_ENERGY:                EnergyChange.ENERGY_GAIN_CRESCENDO,
            Exposition.TR_THEME_DOMINANT_LOCK:         True,
            Exposition.TR_THEME_CHROMATIC_PREDOMINANT: True,
            Exposition.TR_THEME_HAMMER_BLOW_COUNT:     3,
            Exposition.TR_THEME_ENDING_KEY:            Key.C_MAJOR,
            Exposition.TR_THEME_ENDING_CADENCE:        Cadence.HC,

            Exposition.MC_TYPE:                        MedialCaesura.GENERAL_PAUSE,
            Exposition.MC_MEASURES:                    measure_number_range(52, 52),

            Exposition.S_THEME_MEASURES:               measure_number_range(53, 88),
            Exposition.S_THEME_KEY:                    Key.G_MAJOR,
            Exposition.S_THEME_OTHER_KEYS:             [Key.G_MINOR],
            Exposition.S_THEME_ENDING_KEY:             Key.G_MAJOR,
            Exposition.EEC_ESC_PRESENT:                True,

            Exposition.C_THEME_MEASURES:               measure_number_range(88, 109),
            Exposition.C_THEME_KEY:                    Key.G_MAJOR,
            Exposition.C_THEME_P_BASED:                True,
        }

    @classmethod
    def development_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Development.MEASURES: measure_number_range(110, 178),

        }

    @classmethod
    def recapitulation_attribute_dict(cls) -> Dict[Field, Any]:
        recap_dict = cls.exposition_attribute_dict()

        recap_changes = {
            Recapitulation.MEASURES:           measure_number_range(178, 298),

            Recapitulation.P_THEME_MEASURES:   measure_number_range(178, 188),

            Recapitulation.TR_THEME_MEASURES:  measure_number_range(188, 204),

            Recapitulation.MC_MEASURES:        measure_number_range(204, 205),
            Recapitulation.MC_TYPE:            MedialCaesura.CAESURA_FILL,

            Recapitulation.S_THEME_MEASURES:   measure_number_range(206, 241),
            Recapitulation.S_THEME_KEY:        Key.C_MAJOR,
            Recapitulation.S_THEME_OTHER_KEYS: [Key.C_MINOR],
            Recapitulation.S_THEME_ENDING_KEY: Key.C_MAJOR,

            Recapitulation.C_THEME_MEASURES:   measure_number_range(241, 259),
        }

        recap_dict.update(recap_changes)
        return recap_dict

    @classmethod
    def coda_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Coda.MEASURES: measure_number_range(259, 298)
        }
