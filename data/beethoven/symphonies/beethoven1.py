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

class Beethoven1(PieceDataClass):
    @classmethod
    def piece_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Piece.ID:            "beethoven1",
            Piece.COMPOSER_ID:   Beethoven.id(),
            Piece.NAME:          "Symphony No. 1",
            Piece.CATALOGUE_ID:  "Op. 21",
            Piece.GLOBAL_KEY:    Key.C_MAJOR,
            Piece.PREMIER_DATE:  date(1800, 4, 2),
            Piece.YEAR_STARTED:  1795,
            Piece.NUM_MOVEMENTS: 4,
            Piece.PIECE_TYPE:    PieceType.SYMPHONY
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
            Sonata.MEASURE_COUNT:            298,
            Sonata.INTRODUCTION_PRESENT:     True,
            Sonata.DEVELOPMENT_PRESENT:      True,
            Sonata.CODA_PRESENT:             True,
            Sonata.EXPOSITION_REPEAT:        True,
            Sonata.DEVELOPMENT_RECAP_REPEAT: False,

            # Delete this attribute if did not render a lilypond image for this sonata
            Sonata.LILYPOND_IMAGE_SETTINGS:  {Sonata.IMAGE_WIDTH: 530}
        }

    @classmethod
    def introduction_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Intro.MEASURES:        MR(1, 12),
            Intro.OPENING_TEMPO:   "Adagio molto",
            Intro.OPENING_KEY:     Key.F_MAJOR,
            Intro.OTHER_KEYS_LIST: [Key.G_MAJOR],
            Intro.ENDING_KEY:      Key.C_MAJOR,
        }

    @classmethod
    def exposition_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Expo.MEASURES:                 MR(13, 109),
            Expo.OPENING_TEMPO:            "Allegro con brio",

            Expo.P_TYPE:                   PThemeType.SELF_CONTAINED_PHRASE,
            Expo.P_MEASURES:               MR(13, 33),
            Expo.P_OPENING_KEY:            Key.C_MAJOR,
            Expo.P_MODULE_PHRASE_DICT:     {
                "P1": PhraseStructure.COMPOUND_SENTENCE,
            },
            Expo.P_MODULE_MEASURES_DICT:   {
                "P1.1": MR(13, 25),
                "P1.2": MR(25, 33),
            },
            Expo.P_PAC_MEASURES_LIST:      [MR(33)],
            Expo.P_ENDING_KEY:             Key.C_MAJOR,
            Expo.P_ENDING_CADENCE:         Cadence.PAC_MAJOR,

            Expo.TR_MEASURES:              MR(33, 52),
            Expo.TR_TYPE:                  TRThemeType.INDEPENDENT_DEVELOPMENTAL,
            Expo.TR_MODULE_MEASURES_DICT:  {
                "TR1.1": MR(33, 41),
                "TR1.2": MR(41, 52)
            },
            Expo.TR_OPENING_KEY:           Key.C_MAJOR,
            Expo.TR_ENERGY:                EnergyChange.ENERGY_GAIN_CRESCENDO,
            Expo.TR_DOMINANT_LOCK:         True,
            Expo.TR_CHROM_PREDOM:          True,
            Expo.TR_HAMMER_COUNT:          3,
            Expo.TR_ENDING_KEY:            Key.C_MAJOR,
            Expo.TR_ENDING_CADENCE:        Cadence.HC,

            Expo.MC_STYLE:                 MC.GENERAL_PAUSE,
            Expo.MC_MEASURES:              MR(52),

            Expo.S_MEASURES:               MR(53, 88),
            Expo.S_TYPE:                   SThemeType.TRI_MODULAR_S,
            Expo.S_MODULE_MEASURES_DICT:   {
                "S1.1": MR(53, 68),
                "S1.2": MR(69, 77),
                "S2.1": MR(77, 88),
            },
            Expo.S_MODULE_PHRASE_DICT:     {
                "S1.1": PhraseStructure.PERIOD,
            },
            Expo.S_MODULE_TYPES_DICT:      {
                "S1.1": SThemeType.LYRICAL_CANTABILE,
                "S1.2": SThemeType.BUSTLING_GALANT,
                "S2.1": SThemeType.MISCHEIVOUS_LAMENT,
            },
            Expo.S_OPENING_KEY:            Key.G_MAJOR,
            Expo.S_ATTEN_PAC_MEAS_LIST:    [MR(77)],
            Expo.S_STRONG_PAC_MEAS_LIST:   [MR(88)],
            Expo.S_OTHER_KEYS_LIST:        [Key.G_MINOR],
            Expo.S_ENDING_KEY:             Key.G_MAJOR,
            Expo.S_ENDING_CADENCE:         Cadence.PAC_MAJOR,
            Expo.EEC_ESC_SECURED:          True,
            Expo.EEC_ESC_MEASURE:          MR(88),

            Expo.C_MEASURES_INCL_C_RT:     MR(88, 109),
            Expo.C_OPENING_KEY:            Key.G_MAJOR,
            Expo.C_MODULE_MEASURES_DICT:   {
                "C1.1": MR(88, 91),
                "C1.2": MR(92, 100),
                "C2.1": MR(100, 106),
            },
            Expo.C_TYPE:                   CThemeType.MULTI_MODULAR_C,
            Expo.C_MODULE_TYPES_DICT:      {
                "C1": CThemeType.FORTE_P_BASED_C,
                "C2": CThemeType.PIANO_AFTERTHOUGHT,
            },
            Expo.C_PAC_MEASURES_LIST:      [MR(100), MR(106)],
            Expo.C_ENDING_KEY_BEFORE_C_RT: Key.G_MAJOR,
            Expo.C_RT_PRESENT:             True,
            Expo.C_RT_MEASURES:            MR(106, 109),
            Expo.C_RT_ENDING_KEY:          Key.C_MAJOR,
        }

    @classmethod
    def development_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Development.MEASURES:        MR(110, 178),
            Development.OPENING_KEY:     Key.A_MAJOR,
            Development.OTHER_KEYS_LIST: [
                Key.G_MAJOR,
                Key.C_MINOR,
                Key.F_MINOR,
                Key.BES_MAJOR,
                Key.EES_MAJOR,
                Key.F_MINOR,
                Key.G_MINOR,
                Key.D_MINOR,
            ],
            Development.ENDING_KEY:      Key.A_MINOR,
            Development.ENDING_CADENCE:  Cadence.HC

        }

    @classmethod
    def recapitulation_attribute_dict(cls) -> Dict[Field, Any]:
        recap_dict = cls.exposition_attribute_dict_without_fields_unlikely_to_be_same()

        recap_updates = {
            Recap.MEASURES:                 MR(178, 298),

            Recap.P_MEASURES:               MR(178, 198),
            Recap.P_COMMENTS:               "P1.2 changed to fragment P1.1.2 motives instead of P1.1.1",
            Recap.P_ENDING_KEY:             Key.G_MAJOR,
            Recap.P_ENDING_CADENCE:         Cadence.PAC_MAJOR,
            Recap.P_PAC_MEASURES_LIST:      [MR(198)],
            Recap.P_MODULE_MEASURES_DICT:   {
                "P1.1":    MR(178, 190),
                "P1.2var": MR(190, 198),
            },
            Recap.TR_MEASURES:              MR(198, 204),
            Recap.TR_MODULE_MEASURES_DICT:  {
                "TR1.1var": MR(198, 204)
            },
            Recap.TR_COMMENTS:              "TR Theme heavily truncated and altered - "
                                            "continues to fragment P1.1.2 16th note motives "
                                            "and TR1.1 headmotive does not appear",
            Recap.TR_ENDING_KEY:            Key.C_MAJOR,
            Recap.MC_MEASURES:              MR(204, 205),
            Recap.MC_STYLE:                 MC.CAESURA_FILL_CASCADE,
            Recap.MC_COMMENTS:              "Caesura Fill added",
            Recap.S_MEASURES:               MR(206, 241),
            Recap.S_ATTEN_PAC_MEAS_LIST:    [MR(230)],
            Recap.S_STRONG_PAC_MEAS_LIST:   [MR(241)],
            Recap.S_MODULE_MEASURES_DICT:   {
                "S1.1": MR(206, 221),
                "S1.2": MR(222, 230),
                "S2.1": MR(230, 241),
            },
            Recap.S_OPENING_KEY:            Key.C_MAJOR,
            Recap.S_OTHER_KEYS_LIST:        [
                Key.C_MINOR
            ],
            Recap.S_ENDING_KEY:             Key.C_MAJOR,
            Recap.EEC_ESC_MEASURE:          MR(241),

            Recap.C_MEASURES_INCL_C_RT:     MR(241, 259),
            Recap.C_OPENING_KEY:            Key.C_MAJOR,
            Recap.C_ENDING_KEY_BEFORE_C_RT: Key.C_MAJOR,
            Recap.C_MODULE_MEASURES_DICT:   {
                "C1.1": MR(241, 244),
                "C1.2": MR(245, 253),
                "C2.1": MR(253, 259),
            },
            Recap.C_PAC_MEASURES_LIST:      [MR(253), MR(259)],
            Recap.C_RT_PRESENT:             False,
            Recap.C_COMMENTS:               "Retransition elided with onset of Coda",
        }

        recap_dict.update(recap_updates)
        return recap_dict

    @classmethod
    def coda_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Coda.MEASURES:        MR(259, 298),
            Coda.OPENING_KEY:     Key.F_MAJOR,
            Coda.OTHER_KEYS_LIST: [Key.D_MINOR],
            Coda.ENDING_KEY:      Key.C_MAJOR,
        }
