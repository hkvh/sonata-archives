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
            Sonata.MEASURE_COUNT:            502,
            Sonata.INTRODUCTION_PRESENT:     False,
            Sonata.DEVELOPMENT_PRESENT:      True,
            Sonata.CODA_PRESENT:             True,
            Sonata.EXPOSITION_REPEAT:        True,
            Sonata.DEVELOPMENT_RECAP_REPEAT: False,

            # Delete this attribute if did not render a lilypond image for this sonata
            Sonata.LILYPOND_IMAGE_SETTINGS:  {Sonata.IMAGE_WIDTH: 460}
        }

    @classmethod
    def introduction_attribute_dict(cls) -> Dict[Field, Any]:
        return {}

    @classmethod
    def exposition_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Exposition.MEASURES:                       measure_number_range(1, 124),
            Exposition.OPENING_TEMPO:                  "Allegro con brio",

            Exposition.P_THEME_MEASURES:               measure_number_range(1, 21),
            Exposition.P_THEME_OPENING_KEY:            Key.C_MINOR,
            Exposition.P_THEME_PHRASE_STRUCTURE:       [PhraseStructure.SENTENCE],
            Exposition.P_THEME_ENDING_CADENCE:         Cadence.HC,

            Exposition.TR_THEME_MEASURES:              measure_number_range(22, 58),
            Exposition.TR_THEME_OPENING_KEY:           Key.C_MINOR,
            Exposition.TR_THEME_CHROMATIC_PREDOMINANT: False,
            Exposition.TR_THEME_HAMMER_BLOW_COUNT:     2,
            Exposition.TR_THEME_ENERGY:                EnergyChange.ENERGY_GAIN_CRESCENDO,
            Exposition.TR_THEME_DOMINANT_LOCK:         False,
            Exposition.TR_THEME_ENDING_KEY:            Key.E_FLAT_MAJOR,
            # Uses A dim7 / C as vii˚7/B-flat
            Exposition.TR_THEME_ENDING_CADENCE:        Cadence.HC_V6,

            Exposition.MC_MEASURES:                    measure_number_range(59, 59),
            Exposition.MC_TYPE:                        MedialCaesura.GENERAL_PAUSE,

            Exposition.S_THEME_MEASURES:               measure_number_range(59, 110),
            Exposition.S_THEME_OPENING_KEY:            Key.E_FLAT_MAJOR,
            Exposition.S_THEME_ENDING_KEY:             Key.E_FLAT_MAJOR,
            Exposition.S_THEME_ENDING_CADENCE:         Cadence.PAC_MAJOR,

            Exposition.EEC_ESC_PRESENT:                True,

            Exposition.C_THEME_MEASURES:               measure_number_range(110, 124),
            Exposition.C_THEME_OPENING_KEY:            Key.E_FLAT_MAJOR,
            Exposition.C_THEME_P_BASED:                True,
            Exposition.C_THEME_ENDING_KEY:             Key.E_FLAT_MAJOR,
            Exposition.C_THEME_ENDING_CADENCE:         Cadence.PAC_MAJOR,
        }

    @classmethod
    def development_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Development.MEASURES:               measure_number_range(125, 248),
            Development.OPENING_KEY:            Key.F_MINOR,
            Development.DEVELOPMENT_OTHER_KEYS: [
                Key.F_MINOR,
                Key.C_MINOR,
                Key.G_MINOR,
                Key.C_MINOR,
                Key.F_MINOR,
            ],
            Development.DEVELOPMENT_ENDING_KEY: Key.C_MINOR,
        }

    @classmethod
    def recapitulation_attribute_dict(cls) -> Dict[Field, Any]:
        recap_dict = cls.exposition_attribute_dict()

        recap_changes = {
            Recapitulation.MEASURES:                        measure_number_range(248, 374),

            Recapitulation.P_THEME_MEASURES:                measure_number_range(248, 268),
            Recapitulation.P_THEME_CHANGE_FROM_EXPOSITION:  "Oboe has mournful Adagio interlude",

            Recapitulation.TR_THEME_MEASURES:               measure_number_range(269, 302),
            Recapitulation.TR_THEME_CHANGE_FROM_EXPOSITION: "Reaches same C dim chord, but resolves differently",

            Recapitulation.MC_MEASURES:                     measure_number_range(302, 302),

            Recapitulation.S_THEME_MEASURES:                measure_number_range(303, 362),
            Recapitulation.S_THEME_OPENING_KEY:             Key.C_MAJOR,
            Recapitulation.S_THEME_ENDING_KEY:              Key.C_MAJOR,

            Recapitulation.C_THEME_MEASURES:                measure_number_range(362, 374),
            Recapitulation.C_THEME_OPENING_KEY:             Key.C_MAJOR,
            Recapitulation.C_THEME_ENDING_KEY:              Key.C_MAJOR,
            Recapitulation.C_THEME_CHANGE_FROM_EXPOSITION:  "Ending Cadence resolution elided into onset of Coda: "
                                                            "I / C Major = V / F minor"
        }

        recap_dict.update(recap_changes)
        return recap_dict

    @classmethod
    def coda_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Coda.MEASURES:    measure_number_range(374, 502),
            Coda.OPENING_KEY: Key.F_MINOR,
            Coda.ENDING_KEY:  Key.C_MINOR,
        }


class Beethoven5_4(SonataDataClass):
    @classmethod
    def sonata_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Sonata.PIECE_ID:                 Beethoven5.id(),
            Sonata.MOVEMENT_NUM:             4,
            Sonata.SONATA_TYPE:              SonataType.TYPE_3,
            Sonata.GLOBAL_KEY:               Key.C_MAJOR,
            Sonata.MEASURE_COUNT:            444,
            Sonata.INTRODUCTION_PRESENT:     False,
            Sonata.DEVELOPMENT_PRESENT:      True,
            Sonata.CODA_PRESENT:             True,
            Sonata.EXPOSITION_REPEAT:        True,
            Sonata.DEVELOPMENT_RECAP_REPEAT: False,

            # Delete this attribute if did not render a lilypond image for this sonata
            Sonata.LILYPOND_IMAGE_SETTINGS:  {Sonata.IMAGE_WIDTH: 620}
        }

    @classmethod
    def introduction_attribute_dict(cls) -> Dict[Field, Any]:
        return {}

    @classmethod
    def exposition_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Exposition.MEASURES:                       measure_number_range(1, 124),
            Exposition.OPENING_TEMPO:                  "Allegro",

            Exposition.P_THEME_MEASURES:               measure_number_range(1, 26),
            Exposition.P_THEME_OPENING_KEY:            Key.C_MAJOR,
            Exposition.P_THEME_ENDING_KEY:             Key.C_MAJOR,

            Exposition.TR_THEME_MEASURES:              measure_number_range(26, 43),
            Exposition.TR_THEME_OPENING_KEY:           Key.C_MAJOR,
            Exposition.TR_THEME_PHRASE_STRUCTURE:      [PhraseStructure.COMPOUND_SENTENCE],
            Exposition.TR_THEME_CHROMATIC_PREDOMINANT: False,
            Exposition.TR_THEME_ENERGY:                EnergyChange.ENERGY_STASIS_FORTE,
            Exposition.TR_THEME_DOMINANT_LOCK:         True,
            Exposition.TR_THEME_ENDING_KEY:            Key.G_MAJOR,
            Exposition.TR_THEME_ENDING_CADENCE:        Cadence.HC,

            Exposition.MC_MEASURES:                    measure_number_range(43, 44),
            Exposition.MC_TYPE:                        MedialCaesura.CAESURA_FILL_CASCADE,

            Exposition.S_THEME_MEASURES:               measure_number_range(45, 63),
            # could be 45 if include S headmotive
            Exposition.S_THEME_OPENING_KEY:            Key.G_MAJOR,
            Exposition.S_THEME_ENDING_KEY:             Key.G_MAJOR,
            Exposition.S_THEME_ENDING_CADENCE:         Cadence.HC,
            Exposition.EEC_ESC_PRESENT:                False,

            Exposition.C_THEME_MEASURES:               measure_number_range(64, 85),
            Exposition.C_THEME_P_BASED:                False,
            Exposition.C_THEME_OPENING_KEY:            Key.G_MAJOR,
            Exposition.C_THEME_ENDING_KEY:             Key.C_MINOR,
        }

    @classmethod
    def development_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Development.MEASURES:               measure_number_range(86, 206),
            Development.OPENING_KEY:            Key.A_MAJOR,
            Development.DEVELOPMENT_OTHER_KEYS: [
                Key.A_MINOR,
                Key.F_MAJOR,
                Key.B_FLAT_MAJOR,
                Key.B_FLAT_MINOR,
                Key.D_FLAT_MAJOR,
                Key.C_MAJOR,
                Key.G_MAJOR,
            ],
            Development.DEVELOPMENT_ENDING_KEY: Key.C_MINOR,

        }

    @classmethod
    def recapitulation_attribute_dict(cls) -> Dict[Field, Any]:
        recap_dict = cls.exposition_attribute_dict()

        recap_changes = {
            Recapitulation.MEASURES:            measure_number_range(207, 374),

            Recapitulation.P_THEME_MEASURES:    measure_number_range(207, 232),

            Recapitulation.TR_THEME_MEASURES:   measure_number_range(232, 252),

            Recapitulation.MC_MEASURES:         measure_number_range(252, 253),

            Recapitulation.S_THEME_MEASURES:    measure_number_range(254, 272),
            # could be 253 if include S headmotive
            Recapitulation.S_THEME_OPENING_KEY: Key.C_MAJOR,
            Recapitulation.S_THEME_ENDING_KEY:  Key.C_MAJOR,

            Recapitulation.C_THEME_MEASURES:    measure_number_range(273, 294),  # or 293 depending on definition
            Recapitulation.C_THEME_OPENING_KEY: Key.C_MAJOR,
            Recapitulation.C_THEME_ENDING_KEY:  Key.C_MAJOR,
        }

        recap_dict.update(recap_changes)
        return recap_dict

    @classmethod
    def coda_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Coda.MEASURES:    measure_number_range(294, 444),  # could also be 295 if treat S headmotive as not coda
            Coda.OPENING_KEY: Key.C_MAJOR,
            Coda.ENDING_KEY:  Key.C_MAJOR,
        }
