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

class Beethoven6(PieceDataClass):
    @classmethod
    def piece_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Piece.ID:             "beethoven6",
            Piece.COMPOSER_ID:    Beethoven.id(),
            Piece.NAME:           "Symphony No. 6",
            Piece.CATALOGUE_ID:   "Op. 68",
            Piece.NICKNAME:       "Pastoral",
            Piece.GLOBAL_KEY:     Key.F_MAJOR,
            Piece.PREMIER_DATE:   date(1808, 12, 22),
            Piece.YEAR_STARTED:   1808,
            Piece.YEAR_COMPLETED: 1808,
            Piece.NUM_MOVEMENTS:  5,
            Piece.PIECE_TYPE:     PieceType.SYMPHONY
        }


#################
# Sonata(s)
#################

class Beethoven6_1(SonataDataClass):
    @classmethod
    def sonata_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Sonata.PIECE_ID:                 Beethoven6.id(),
            Sonata.MOVEMENT_NUM:             1,
            Sonata.SONATA_TYPE:              SonataType.TYPE_3,
            Sonata.GLOBAL_KEY:               Key.F_MAJOR,
            Sonata.MEASURE_COUNT:            512,
            Sonata.INTRODUCTION_PRESENT:     False,
            Sonata.DEVELOPMENT_PRESENT:      True,
            Sonata.CODA_PRESENT:             True,
            Sonata.EXPOSITION_REPEAT:        True,
            Sonata.DEVELOPMENT_RECAP_REPEAT: False,

            # Delete this attribute if did not render a lilypond image for this sonata
            Sonata.LILYPOND_IMAGE_SETTINGS:  {Sonata.IMAGE_WIDTH: 660}
        }

    @classmethod
    def introduction_attribute_dict(cls) -> Dict[Field, Any]:
        return {

        }

    @classmethod
    def exposition_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Expo.MEASURES:                 MR(1, 138),
            Expo.OPENING_TEMPO:            "Allegro ma non troppo",

            Expo.P_MEASURES:               MR(1, 28),
            Expo.P_TYPE:                   PThemeType.GRAND_ANTECEDENT,
            Expo.P_MODULE_MEASURES_DICT:   {
                "P1.1": MR(1, 4),
                "P1.2": MR(5, 8),
                "P1.3": MR(9, 16),
                "P1.4": MR(16, 28),
            },
            Expo.P_MODULE_PHRASE_DICT:     {
                "P1.1": PhraseStructure.ANTECEDENT,
                "P1.2": PhraseStructure.PRESENTATION,
                "P1.3": PhraseStructure.PRESENTATION,
                "P1.4": PhraseStructure.CONTINUATION,
            },
            Expo.P_PAC_MEASURES_LIST:      [],
            Expo.P_OPENING_KEY:            Key.F_MAJOR,
            Expo.P_ENDING_KEY:             Key.F_MAJOR,
            Expo.P_ENDING_CADENCE:         Cadence.HC,

            Expo.TR_MEASURES:              MR(29, 53),
            Expo.TR_TYPE:                  TRThemeType.INDEPENDENT_DEVELOPMENTAL,
            Expo.TR_MODULE_MEASURES_DICT:  {
                "TR1.1": MR(29, 37),
                "TR1.2": MR(37, 53),
            },
            Expo.TR_OPENING_KEY:           Key.F_MAJOR,
            Expo.TR_ENERGY:                EnergyChange.ENERGY_STASIS_FORTE,
            Expo.TR_HAMMER_COUNT:          0,
            Expo.TR_DOMINANT_LOCK:         False,
            Expo.TR_CHROM_PREDOM:          False,
            Expo.TR_ENDING_KEY:            Key.F_MAJOR,
            Expo.TR_ENDING_CADENCE:        Cadence.IAC_MAJOR,

            Expo.MC_MEASURES:              MR(53, 66),
            Expo.MC_STYLE:                 MC.DEFORMATION_CAESURA_FILL,
            Expo.MC_FILL_KEY:              Key.F_MAJOR,
            Expo.MC_COMMENTS:              "Series of pause + fill gestures surround tripleted motives; "
                                           "it is a deformational cascade of MC moments but the net "
                                           "effect is still the MC that is clearly opening up S space",

            Expo.S_MEASURES:               MR(67, 115),
            Expo.S_TYPE:                   SThemeType.MULTI_MODULAR_S,
            Expo.S_MODULE_TYPES_DICT:      {
                "S1.1": SThemeType.LYRICAL_CANTABILE,
                "S1.2": SThemeType.FORTE_PIANO_ALTERNATING,
            },
            Expo.S_MODULE_MEASURES_DICT:   {
                "S1.1": MR(67, 93),
                "S1.2": MR(93, 115),
            },
            Expo.S_OPENING_KEY:            Key.C_MAJOR,
            Expo.S_EVADED_PAC_MEAS_LIST:   [MR(100), MR(107), MR(111)],
            Expo.S_STRONG_PAC_MEAS_LIST:   [MR(115)],
            Expo.S_ENDING_KEY:             Key.C_MAJOR,
            Expo.S_ENDING_CADENCE:         Cadence.PAC_MAJOR,

            Expo.EEC_ESC_SECURED:          True,
            Expo.EEC_ESC_MEASURE:          MR(115),

            Expo.C_MEASURES_INCL_C_RT:     MR(115, 138),
            Expo.C_TYPE:                   CThemeType.MULTI_MODULAR_C,
            Expo.C_RT_PRESENT:             True,
            Expo.C_MODULE_MEASURES_DICT:   {
                "C1.1": MR(115, 127),
                "C1.2": MR(127, 135)
            },
            Expo.C_MODULE_TYPES_DICT:      {
                "C1.1": CThemeType.FORTE_P_DERIVATION_C,
                "C1.2": CThemeType.PIANO_AFTERTHOUGHT,
            },
            Expo.C_OPENING_KEY:            Key.C_MAJOR,
            Expo.C_ENDING_KEY_BEFORE_C_RT: Key.C_MAJOR,
            Expo.C_RT_MEASURES:            MR(135, 138),
            Expo.C_RT_ENDING_KEY:          Key.F_MAJOR,
            Expo.C_COMMENTS:               "C1 ends in C Major but 4-bar C-RT veers back to F Major",
        }

    @classmethod
    def development_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Development.MEASURES:        MR(139, 278),
            Development.OPENING_KEY:     Key.F_MAJOR,
            Development.OTHER_KEYS_LIST: [
                Key.BES_MAJOR,
                Key.D_MAJOR,  # This is a long-enough V of G that it feels like its own key
                Key.G_MAJOR,
                Key.E_MAJOR,  # This is a long-enough V of A that it feels like its own key
                Key.A_MAJOR,
                Key.G_MINOR,
                Key.C_MAJOR,
                Key.F_MAJOR,  # Ends on clear subdominant (almost like an a half cadence ending on IV)
            ],
            Development.ENDING_KEY:      Key.BES_MAJOR,
        }

    @classmethod
    def recapitulation_attribute_dict(cls) -> Dict[Field, Any]:
        recap_dict = cls.exposition_attribute_dict_without_fields_unlikely_to_be_same()

        recap_updates = {
            Recap.COMMENTS:                 "Plagal Cadence leads to soft, almost hidden "
                                            "onset of Recapitulation: "
                                            "developmental counter-melodies over P1.0 and P1.1 "
                                            "make recap-effect subtle until dramatic TR emergence",
            Recap.MEASURES:                 MR(279, 417),

            Recap.P_MEASURES:               MR(279, 311),
            Recap.P_MODULE_MEASURES_DICT:   {
                "P1.1": MR(279, 288),
                "P1.2": MR(289, 292),
                "P1.3": MR(293, 300),
                "P1.4": MR(300, 311)
            },
            Recap.P_COMMENTS:               "P1.1 has new violin I countermelody and the half-cadence"
                                            "fermata is expanded into a multi-measure figuration; "
                                            "P1.2-P1.4 contain a novel tripleted ostinato "
                                            "countermelody throughout",

            Recap.TR_MEASURES:              MR(312, 328),
            Recap.TR_MODULE_MEASURES_DICT:  {
                "TR1.2": MR(312, 328)
            },
            Recap.TR_ENDING_KEY:            Key.F_MAJOR,
            Recap.TR_COMMENTS:              "TR1.1 elided completely in favor of more boisterous TR1.2",

            Recap.MC_MEASURES:              MR(328, 345),
            Recap.MC_COMMENTS:              "MC is slightly extended with additional "
                                            "tripleted gestures + fill",

            Recap.S_MEASURES:               MR(346, 394),
            Recap.S_MODULE_MEASURES_DICT:   {
                "S1.1": MR(346, 372),
                "S1.2": MR(372, 394),
            },
            Recap.S_OPENING_KEY:            Key.F_MAJOR,
            Recap.S_EVADED_PAC_MEAS_LIST:   [MR(379), MR(386), MR(390)],
            Recap.S_STRONG_PAC_MEAS_LIST:   [MR(394)],
            Recap.S_ENDING_KEY:             Key.F_MAJOR,
            Recap.EEC_ESC_MEASURE:          MR(394),

            Recap.C_MEASURES_INCL_C_RT:     MR(394, 417),
            Recap.C_MODULE_MEASURES_DICT:   {
                "C1.1": MR(394, 406),
                "C1.2": MR(406, 414)
            },
            Recap.C_OPENING_KEY:            Key.F_MAJOR,
            Recap.C_RT_MEASURES:            MR(414, 417),
            Recap.C_ENDING_KEY_BEFORE_C_RT: Key.F_MAJOR,
            Recap.C_RT_ENDING_KEY:          Key.BES_MAJOR,
            Recap.C_COMMENTS:               "C transposed up a fourth for tonic resolution (as "
                                            "expected), leading to C Major C1. However, "
                                            "this creates a problem for the C-RT gesture that "
                                            "was already going to tonic in exposition, so the exact "
                                            "transposition accidentally veers us to the subdominant!"
        }

        recap_dict.update(recap_updates)
        return recap_dict

    @classmethod
    def coda_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Coda.MEASURES:    MR(418, 512),
            Coda.P_RECALLED:  True,
            Coda.OPENING_KEY: Key.BES_MAJOR,
            Coda.ENDING_KEY:  Key.F_MAJOR,
        }
