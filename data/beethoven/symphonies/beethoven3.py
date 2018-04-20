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

class Beethoven3(PieceDataClass):
    @classmethod
    def piece_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Piece.ID:             "beethoven3",
            Piece.COMPOSER_ID:    Beethoven.id(),
            Piece.NAME:           "Symphony No. 3",
            Piece.CATALOGUE_ID:   "Op. 55",
            Piece.NICKNAME:       "Eroica",
            Piece.GLOBAL_KEY:     Key.EES_MAJOR,
            Piece.PREMIER_DATE:   date(1805, 4, 7),
            Piece.YEAR_STARTED:   1802,
            Piece.YEAR_COMPLETED: 1804,
            Piece.NUM_MOVEMENTS:  4,
            Piece.PIECE_TYPE:     PieceType.SYMPHONY
        }


#################
# Sonata(s)
#################

class Beethoven3_1(SonataDataClass):
    @classmethod
    def sonata_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Sonata.PIECE_ID:                 Beethoven3.id(),
            Sonata.MOVEMENT_NUM:             1,
            Sonata.SONATA_TYPE:              SonataType.TYPE_3,
            Sonata.GLOBAL_KEY:               Key.EES_MAJOR,
            Sonata.MEASURE_COUNT:            701,
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
            Intro.MEASURES:      MR(1, 2),
            Intro.OPENING_TEMPO: "Adagio molto",
            Intro.OPENING_KEY:   Key.EES_MAJOR,
            Intro.ENDING_KEY:    Key.EES_MAJOR,
        }

    @classmethod
    def exposition_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Expo.MEASURES:                 MR(3, 153),
            Expo.OPENING_TEMPO:            "Allegro con brio",

            Expo.P_MEASURES:               MR(3, 37),
            Expo.P_TYPE:                   PThemeType.SELF_CONTAINED_PHRASE,
            Expo.P_MODULE_MEASURES_DICT:   {
                "P1.1": MR(3, 6),
                "P1.2": MR(7, 11),
                "P1.3": MR(12, 15),
                "P2.1": MR(15, 22),
                "P2.2": MR(23, 37),
            },
            Expo.P_OPENING_KEY:            Key.EES_MAJOR,
            Expo.P_ENDING_KEY:             Key.EES_MAJOR,
            Expo.P_ENDING_CADENCE:         Cadence.PAC_MAJOR,
            Expo.P_PAC_MEASURES_LIST:      [MR(15), MR(37)],

            Expo.TR_MEASURES:              MR(37, 45),
            Expo.TR_TYPE:                  TRThemeType.DISSOLVING_RESTATEMENT,
            Expo.TR_MODULE_MEASURES_DICT:  {
                "TR1.1": MR(37, 45),
            },
            Expo.TR_OPENING_KEY:           Key.EES_MAJOR,
            Expo.TR_ENERGY:                EnergyChange.ENERGY_STASIS_FORTE,
            Expo.TR_HAMMER_COUNT:          0,
            Expo.TR_CHROM_PREDOM:          True,
            Expo.TR_ENDING_KEY:            Key.BES_MAJOR,
            Expo.TR_ENDING_CADENCE:        Cadence.HC,

            Expo.MC_STYLE:                 MC.CAESURA_FILL_CASCADE_AS_S0,
            Expo.MC_MEASURES:              MR(45, 56),

            Expo.S_MEASURES:               MR(45, 83),
            Expo.S_TYPE:                   SThemeType.MULTI_MODULAR_S,
            Expo.S_MODULE_MEASURES_DICT:   {
                "S0":   MR(45, 57),
                "S1.1": MR(57, 65),
                "S1.2": MR(65, 74),
                "S1.3": MR(75, 83),
            },
            Expo.S_MODULE_TYPES_DICT:      {
                "S0":   SThemeType.LYRICAL_CANTABILE,
                "S1.1": SThemeType.LYRICAL_CANTABILE,
                "S1.2": SThemeType.FURIOUS_STORMY,
                "S1.3": SThemeType.HEROIC_CADENTIAL,
            },
            Expo.S_STRONG_PAC_MEAS_LIST:   [MR(83)],
            Expo.S_OPENING_KEY:            Key.BES_MAJOR,
            Expo.S_ENDING_KEY:             Key.BES_MAJOR,
            Expo.S_ENDING_CADENCE:         Cadence.PAC_MAJOR,

            Expo.EEC_ESC_SECURED:          True,
            Expo.EEC_ESC_MEASURE:          MR(83),

            Expo.C_MEASURES_INCL_C_RT:     MR(83, 153),
            Expo.C_TYPE:                   CThemeType.MULTI_MODULAR_C,
            Expo.C_MODULE_MEASURES_DICT:   {
                "C0.1": MR(83, 99),
                "C0.2": MR(99, 109),
                "C1.1": MR(109, 123),
                "C1.2": MR(123, 131),
                "C1.3": MR(132, 144),
                "C2.1": MR(144, 148),
                "C2.2": MR(148, 153),
            },
            Expo.C_MODULE_TYPES_DICT:      {
                "C0.1": CThemeType.RETREAT_FROM_ACTION,
                "C0.2": CThemeType.CRESCENDO_ONSET,
                "C1.1": CThemeType.FORTE_P_DERIVATION_C,
                "C1.2": CThemeType.FORTE_P_DERIVATION_C,
                "C1.3": [CThemeType.PIANO_P_DERIVATION_C, CThemeType.CRESCENDO_ONSET],
                "C2.1": CThemeType.FORTE_P_DERIVATION_C,
                "C2.2": CThemeType.PIANO_P_BASED_C,
            },
            Expo.C_OPENING_KEY:            Key.BES_MAJOR,
            Expo.C_PAC_MEASURES_LIST:      [MR(144)],
            Expo.C_ENDING_KEY_BEFORE_C_RT: Key.BES_MAJOR,
            Expo.C_RT_PRESENT:             False,
        }

    @classmethod
    def development_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Development.MEASURES:                  MR(154, 398),
            Development.OPENING_KEY:               Key.C_MAJOR,
            Development.OTHER_KEYS_LIST:           [
                Key.C_MINOR,
                Key.CIS_MINOR,
                Key.D_MINOR,
                Key.G_MINOR,
                Key.AES_MAJOR,
                Key.F_MINOR,
                Key.G_MINOR,
                Key.A_MINOR,
                Key.E_MINOR,
                Key.C_MAJOR,
                Key.C_MINOR,
                Key.EES_MAJOR,
                Key.EES_MINOR,
                Key.GES_MAJOR,
                Key.EES_MINOR,
                Key.CES_MAJOR,
                Key.EES_MINOR,
            ],
            Development.DEVELOPMENT_THEME_PRESENT: True,
            Development.DEVELOPMENT_THEME_KEYS:    [
                Key.E_MINOR,
                Key.EES_MINOR,
            ],
            Development.ENDING_KEY:                Key.EES_MAJOR,
            Development.ENDING_CADENCE:            Cadence.PAC_MAJOR

        }

    @classmethod
    def recapitulation_attribute_dict(cls) -> Dict[Field, Any]:
        recap_dict = cls.exposition_attribute_dict_without_fields_unlikely_to_be_same()

        recap_updates = {
            Recap.MEASURES:                 MR(398, 556),

            Recap.P_MEASURES:               MR(398, 430),
            Recap.P_PAC_MEASURES_LIST:      [MR(408), MR(430)],
            Recap.P_MODULE_MEASURES_DICT:   {
                "P1.1":    MR(398, 401),
                "P1.2":    MR(402, 405),
                "P1.3var": MR(406, 408),
                "P2.1var": MR(408, 425),
                "P2.2var": MR(426, 430),
            },
            Recap.P_COMMENTS:               "End of P1.2 leads to modified P1.3 that cadences into "
                                            "F major. P2.1 is elongated in non-tonic keys of F and"
                                            "Db Major and almost all of P2.2 is elided except final"
                                            "build-up into the PAC that begins TR",
            Recap.P_OTHER_KEYS_LIST:        [
                Key.F_MAJOR,
                Key.DES_MAJOR,
            ],
            Recap.P_ENDING_KEY:             Key.EES_MAJOR,

            Recap.TR_MEASURES:              MR(430, 448),
            Expo.TR_MODULE_MEASURES_DICT:   {
                "TR1.1": MR(430, 448),
            },
            Recap.TR_ENDING_KEY:            Key.EES_MAJOR,
            Recap.TR_COMMENTS:              "Middle section lengthened",

            Recap.MC_MEASURES:              MR(448, 459),

            Recap.S_MEASURES:               MR(448, 486),
            Recap.S_MODULE_MEASURES_DICT:   {
                "S0":   MR(448, 460),
                "S1.1": MR(460, 468),
                "S1.2": MR(468, 477),
                "S1.3": MR(478, 486),
            },
            Recap.S_STRONG_PAC_MEAS_LIST:   [MR(486)],
            Recap.S_OPENING_KEY:            Key.EES_MAJOR,
            Recap.S_ENDING_KEY:             Key.EES_MAJOR,
            Recap.EEC_ESC_MEASURE:          MR(486),

            Recap.C_MEASURES_INCL_C_RT:     MR(486, 556),
            Recap.C_MODULE_MEASURES_DICT:   {
                "C0.1": MR(486, 502),
                "C0.2": MR(502, 512),
                "C1.1": MR(512, 526),
                "C1.2": MR(526, 534),
                "C1.3": MR(535, 547),
                "C2.1": MR(547, 551),
                "C2.2": MR(551, 556),
            },
            Recap.C_PAC_MEASURES_LIST:      [MR(547)],
            Recap.C_OPENING_KEY:            Key.EES_MAJOR,
            Recap.C_ENDING_KEY_BEFORE_C_RT: Key.EES_MAJOR
        }

        recap_dict.update(recap_updates)
        return recap_dict

    @classmethod
    def coda_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Coda.MEASURES:                   MR(557, 701),
            Coda.P_RECALLED:                 True,
            Coda.DEVELOPMENT_THEME_RECALLED: True,
            Coda.OPENING_KEY:                Key.DES_MAJOR,
            Coda.OTHER_KEYS_LIST:            [
                Key.C_MAJOR,
                Key.F_MINOR,
                Key.EES_MINOR,
            ],
            Coda.ENDING_KEY:                 Key.EES_MAJOR,
        }
