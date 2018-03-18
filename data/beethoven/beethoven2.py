#!/usr/bin/env python
from datetime import date

from data.composers import Beethoven
from database_design.sonata_data_classes import PieceDataClass, SonataDataClass
from database_design.sonata_table_specs import *
from enums.key_enums import Key
from enums.measure_enums import *
from enums.sonata_enums import *
from general_utils.sql_utils import Field


#################
# Piece
#################

class Beethoven2(PieceDataClass):
    @classmethod
    def piece_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Piece.ID:             "beethoven2",
            Piece.COMPOSER_ID:    Beethoven.id(),
            Piece.NAME:           "Symphony No. 2",
            Piece.CATALOGUE_ID:   "Op. 36",
            Piece.GLOBAL_KEY:     Key.D_MAJOR,
            Piece.PREMIER_DATE:   date(1802, 4, 5),
            Piece.YEAR_STARTED:   1801,
            Piece.YEAR_COMPLETED: 1802,
            Piece.NUM_MOVEMENTS:  4,
            Piece.PIECE_TYPE:     PieceType.SYMPHONY
        }


#################
# Sonata(s)
#################

class Beethoven2_1(SonataDataClass):
    @classmethod
    def sonata_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Sonata.PIECE_ID:                 Beethoven2.id(),
            Sonata.MOVEMENT_NUM:             1,
            Sonata.SONATA_TYPE:              SonataType.TYPE_3,
            Sonata.GLOBAL_KEY:               Key.D_MAJOR,
            Sonata.MEASURE_COUNT:            360,
            Sonata.INTRODUCTION_PRESENT:     True,
            Sonata.DEVELOPMENT_PRESENT:      True,
            Sonata.CODA_PRESENT:             True,
            Sonata.EXPOSITION_REPEAT:        True,
            Sonata.DEVELOPMENT_RECAP_REPEAT: False,

            # Delete this attribute if did not render a lilypond image for this sonata
            Sonata.LILYPOND_IMAGE_SETTINGS:  {Sonata.IMAGE_WIDTH: 560}
        }

    @classmethod
    def introduction_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Introduction.MEASURES:                MeasureRange(1, 33),
            Introduction.OPENING_TEMPO:           "Adagio molto",
            Introduction.OPENING_KEY:             Key.D_MAJOR,
            Introduction.INTRODUCTION_OTHER_KEYS: [
                Key.B_FLAT_MAJOR,
                Key.D_MINOR,
            ],
            Introduction.ENDING_KEY:              Key.D_MAJOR,
        }

    @classmethod
    def exposition_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Exposition.MEASURES:                   MeasureRange(34, 133),
            Exposition.OPENING_TEMPO:              "Allegro con brio",

            Exposition.P_THEME_MEASURES:           MeasureRange(34, 57),
            Exposition.P_THEME_PHRASE_STRUCTURE: {
                'P1': PhraseStructure.COMPOUND_SENTENCE,
            },
            Exposition.P_THEME_OPENING_KEY:        Key.D_MAJOR,
            Exposition.P_THEME_ENDING_KEY:         Key.D_MINOR,
            Exposition.P_THEME_ENDING_CADENCE:     Cadence.IAC_V6_i,

            Exposition.TR_THEME_MEASURES:          MeasureRange(57, 71),
            # Debating whether to start TR on A minor section at m. 61
            # (would be similar to recap recap D minor start at m. 233
            # – no other recap option since no m. 57-60 corresponding measures)
            # But since TR generally modulates, I like the m. 57 start
            Exposition.TR_THEME_OPENING_KEY:       Key.D_MINOR,
            Exposition.TR_THEME_ENERGY:            EnergyChange.ENERGY_GAIN_CRESCENDO,
            Exposition.TR_THEME_DOMINANT_LOCK:     True,
            Exposition.TR_THEME_HAMMER_BLOW_COUNT: 0,
            Exposition.TR_THEME_ENDING_KEY:        Key.A_MINOR,
            Exposition.TR_THEME_ENDING_CADENCE:    Cadence.HC,

            Exposition.MC_TYPE:                    MedialCaesura.CAESURA_FILL_CASCADE,
            Exposition.MC_MEASURES:                MeasureRange(71, 72),

            Exposition.S_THEME_MEASURES:           MeasureRange(73, 112),
            Exposition.S_THEME_PHRASE_STRUCTURE:   {
                'S1':   PhraseStructure.COMPOUND_PERIOD_OF_PERIODS,
            },
            Exposition.S_THEME_OPENING_KEY:        Key.A_MAJOR,
            Exposition.S_THEME_ENDING_KEY:         Key.A_MAJOR,
            Exposition.S_THEME_ENDING_CADENCE:     Cadence.IAC_MAJOR,
            Exposition.EEC_ESC_PRESENT:            True,
            Exposition.EEC_ESC_STRENGTH:           "Flute plays soprano 3ˆ, but otherwise feels like strong PAC",

            Exposition.C_THEME_MEASURES:           MeasureRange(112, 133),
            Exposition.C_THEME_OPENING_KEY:        Key.A_MAJOR,
            Exposition.C_THEME_OTHER_KEYS:         [Key.D_MINOR],
            Exposition.C_THEME_P_BASED:            True,
            Exposition.C_THEME_ENDING_KEY:         Key.D_MAJOR
        }

    @classmethod
    def development_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Development.MEASURES:                   MeasureRange(134, 216),
            Development.OPENING_KEY:                Key.D_MINOR,
            Development.DEVELOPMENT_ENDING_KEY:     Key.D_MAJOR,
            Development.DEVELOPMENT_ENDING_CADENCE: Cadence.PAC_MAJOR

        }

    @classmethod
    def recapitulation_attribute_dict(cls) -> Dict[Field, Any]:
        recap_dict = cls.exposition_attribute_dict()

        recap_changes = {
            Recapitulation.MEASURES:                        MeasureRange(216, 298),

            Recapitulation.P_THEME_MEASURES:                MeasureRange(216, 233),
            Recapitulation.P_THEME_ENDING_KEY:              Key.D_MAJOR,
            Recapitulation.P_THEME_ENDING_CADENCE:          Cadence.HC,

            Recapitulation.TR_THEME_MEASURES:               MeasureRange(233, 243),
            Recapitulation.TR_THEME_OPENING_KEY:            Key.D_MINOR,

            Recapitulation.TR_THEME_ENDING_KEY:             Key.D_MINOR,
            Recapitulation.TR_THEME_CHANGE_FROM_EXPOSITION: "TR Theme beginning elided",
            # If decide to move exposition TR to m. 61, then TR exactly like recap

            Recapitulation.MC_MEASURES:                     MeasureRange(243, 244),

            Recapitulation.S_THEME_MEASURES:                MeasureRange(245, 284),
            Recapitulation.S_THEME_OPENING_KEY:             Key.D_MAJOR,
            Recapitulation.S_THEME_ENDING_KEY:              Key.D_MAJOR,

            Recapitulation.C_THEME_MEASURES:                MeasureRange(284, 305),
            Exposition.C_THEME_OPENING_KEY:                 Key.D_MAJOR,
            Exposition.C_THEME_OTHER_KEYS:                  [Key.G_MINOR],
            Exposition.C_THEME_ENDING_KEY:                  Key.D_MAJOR
        }

        recap_dict.update(recap_changes)
        return recap_dict

    @classmethod
    def coda_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Coda.MEASURES:    MeasureRange(306, 360),
            Coda.OPENING_KEY: Key.G_MAJOR,
            Coda.ENDING_KEY:  Key.D_MAJOR,
        }
