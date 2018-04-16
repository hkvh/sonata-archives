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
            Exposition.MEASURES:                         MR(1, 138),
            Exposition.OPENING_TEMPO:                    "Allegro ma non troppo",

            Exposition.P_THEME_MEASURES:                 MR(1, 28),
            Exposition.P_THEME_TYPE:                     PThemeType.GRAND_ANTECEDENT,
            Exposition.P_MODULE_MEASURES_DICT:           {
                "P1.1": MR(1, 4),
                "P1.2": MR(5, 8),
                "P1.3": MR(9, 16),
                "P1.4": MR(16, 28),
            },
            Exposition.P_MODULE_PHRASE_DICT:             {
                "P1.1": PhraseStructure.ANTECEDENT,
                "P1.2": PhraseStructure.PRESENTATION,
                "P1.3": PhraseStructure.PRESENTATION,
                "P1.4": PhraseStructure.CONTINUATION,
            },
            Exposition.P_THEME_PAC_MEASURES_LIST:        [],
            Exposition.P_THEME_OPENING_KEY:              Key.F_MAJOR,
            Exposition.P_THEME_ENDING_KEY:               Key.F_MAJOR,
            Exposition.P_THEME_ENDING_CADENCE:           Cadence.HC,

            Exposition.TR_THEME_MEASURES:                MR(29, 53),
            Exposition.TR_THEME_TYPE:                    TRThemeType.INDEPENDENT_DEVELOPMENTAL,
            Exposition.TR_MODULE_MEASURES_DICT:          {
                "TR1.1": MR(29, 37),
                "TR1.2": MR(37, 53),
            },
            Exposition.TR_THEME_OPENING_KEY:             Key.F_MAJOR,
            Exposition.TR_THEME_ENERGY:                  EnergyChange.ENERGY_STASIS_FORTE,
            Exposition.TR_THEME_HAMMER_BLOW_COUNT:       0,
            Exposition.TR_THEME_DOMINANT_LOCK:           False,
            Exposition.TR_THEME_CHROMATIC_PREDOMINANT:   False,
            Exposition.TR_THEME_ENDING_KEY:              Key.F_MAJOR,
            Exposition.TR_THEME_ENDING_CADENCE:          Cadence.IAC_MAJOR,

            Exposition.MC_MEASURES:                      MR(53, 66),
            Exposition.MC_STYLE:                         MC.DEFORMATION_CAESURA_FILL,
            Exposition.MC_FILL_KEY:                      Key.F_MAJOR,
            Exposition.MC_COMMENTS:                      "Series of pause + fill gestures surround tripleted motives; "
                                                         "it is a deformational cascade of MC moments but the net "
                                                         "effect is still the MC that is clearly opening up S space",

            Exposition.S_THEME_MEASURES:                 MR(67, 115),
            Exposition.S_THEME_TYPE:                     SThemeType.MULTI_MODULAR_S,
            Exposition.S_MODULE_TYPES_DICT:              {
                "S1.1": SThemeType.LYRICAL_CANTABILE,
                "S1.2": SThemeType.FORTE_PIANO_ALTERNATING,
            },
            Exposition.S_MODULE_MEASURES_DICT:           {
                "S1.1": MR(67, 93),
                "S1.2": MR(93, 115),
            },
            Exposition.S_THEME_OPENING_KEY:              Key.C_MAJOR,
            Exposition.S_THEME_EVADED_PAC_MEASURES_LIST: [MR(100), MR(107), MR(111)],
            Exposition.S_THEME_STRONG_PAC_MEASURES_LIST: [MR(115)],
            Exposition.S_THEME_ENDING_KEY:               Key.C_MAJOR,
            Exposition.S_THEME_ENDING_CADENCE:           Cadence.PAC_MAJOR,

            Exposition.EEC_ESC_SECURED:                  True,
            Exposition.EEC_ESC_MEASURE:                  MR(115),

            Exposition.C_THEME_MEASURES_INCL_C_RT:       MR(115, 138),
            Exposition.C_THEME_TYPE:                     CThemeType.MULTI_MODULAR_C,
            Exposition.C_RT_PRESENT:                     True,
            Exposition.C_MODULE_MEASURES_DICT:           {
                "C1.1": MR(115, 127),
                "C1.2": MR(127, 135)
            },
            Exposition.C_MODULE_TYPES_DICT:              {
                "C1.1": CThemeType.FORTE_P_DERIVATION_C,
                "C1.2": CThemeType.PIANO_AFTERTHOUGHT,
            },
            Exposition.C_THEME_OPENING_KEY:              Key.C_MAJOR,
            Exposition.C_THEME_ENDING_KEY_BEFORE_C_RT:   Key.C_MAJOR,
            Exposition.C_RT_MEASURES:                    MR(135, 138),
            Exposition.C_RT_ENDING_KEY:                  Key.F_MAJOR,
            Exposition.C_THEME_COMMENTS:                 "C1 ends in C Major but 4-bar C-RT veers back to F Major",
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
            Recapitulation.COMMENTS:                         "Plagal Cadence leads to soft, almost hidden "
                                                             "onset of Recapitulation: "
                                                             "developmental counter-melodies over P1.0 and P1.1 "
                                                             "make recap-effect subtle until dramatic TR emergence",
            Recapitulation.MEASURES:                         MR(279, 417),

            Recapitulation.P_THEME_MEASURES:                 MR(279, 311),
            Recapitulation.P_MODULE_MEASURES_DICT:           {
                "P1.1": MR(279, 288),
                "P1.2": MR(289, 292),
                "P1.3": MR(293, 300),
                "P1.4": MR(300, 311)
            },
            Recapitulation.P_THEME_CHANGE_FROM_EXPOSITION:   "P1.1 has new violin I countermelody and the half-cadence"
                                                             "fermata is expanded into a multi-measure figuration; "
                                                             "P1.2-P1.4 contain a novel tripleted ostinato "
                                                             "countermelody throughout",

            Recapitulation.TR_THEME_MEASURES:                MR(312, 328),
            Recapitulation.TR_MODULE_MEASURES_DICT:          {
                "TR1.2": MR(312, 328)
            },
            Recapitulation.TR_THEME_ENDING_KEY:              Key.F_MAJOR,
            Recapitulation.TR_THEME_CHANGE_FROM_EXPOSITION:  "TR1.1 elided completely in favor of more boisterous TR1.2",

            Recapitulation.MC_MEASURES:                      MR(328, 345),
            Recapitulation.MC_CHANGE_FROM_EXPOSITION:        "MC is slightly extended with additional "
                                                             "tripleted gestures + fill",

            Recapitulation.S_THEME_MEASURES:                 MR(346, 394),
            Recapitulation.S_MODULE_MEASURES_DICT:           {
                "S1.1": MR(346, 372),
                "S1.2": MR(372, 394),
            },
            Recapitulation.S_THEME_OPENING_KEY:              Key.F_MAJOR,
            Recapitulation.S_THEME_EVADED_PAC_MEASURES_LIST: [MR(379), MR(386), MR(390)],
            Recapitulation.S_THEME_STRONG_PAC_MEASURES_LIST: [MR(394)],
            Recapitulation.S_THEME_ENDING_KEY:               Key.F_MAJOR,
            Recapitulation.EEC_ESC_MEASURE:                  MR(394),

            Recapitulation.C_THEME_MEASURES_INCL_C_RT:       MR(394, 417),
            Recapitulation.C_MODULE_MEASURES_DICT:           {
                "C1.1": MR(394, 406),
                "C1.2": MR(406, 414)
            },
            Recapitulation.C_THEME_OPENING_KEY:              Key.F_MAJOR,
            Recapitulation.C_RT_MEASURES:                    MR(414, 417),
            Recapitulation.C_THEME_ENDING_KEY_BEFORE_C_RT:   Key.F_MAJOR,
            Recapitulation.C_RT_ENDING_KEY:                  Key.BES_MAJOR,
            Recapitulation.C_THEME_CHANGE_FROM_EXPOSITION:   "C transposed up a fourth for tonic resolution (as "
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
            Coda.MEASURES:         MR(418, 512),
            Coda.P_THEME_RECALLED: True,
            Coda.OPENING_KEY:      Key.BES_MAJOR,
            Coda.ENDING_KEY:       Key.F_MAJOR,
        }
