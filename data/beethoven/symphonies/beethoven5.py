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
            Exposition.MEASURES:                       MR(1, 124),
            Exposition.OPENING_TEMPO:                  "Allegro con brio",

            Exposition.P_THEME_MEASURES:               MR(1, 21),
            Exposition.P_THEME_OPENING_KEY:            Key.C_MINOR,
            Exposition.P_THEME_TYPE:                   PThemeType.GRAND_ANTECEDENT,
            Exposition.P_MODULE_MEASURES_DICT:         {
                "P0":   MR(1, 5),
                "P1.1": MR(6, 14),
                "P1.2": MR(14, 21)
            },
            Exposition.P_THEME_COMMENTS:               "I am calling mm. 1-5 P0 since it is an opening motto cordoned "
                                                       "off from the rest of P1, "
                                                       "but it is a somewhat unusual P0 case since P1.1 "
                                                       "is obviously completely derived from P0. "
                                                       "(Hepokoski calls it P1.0 which is also defensible)",
            Exposition.P_MODULE_PHRASE_DICT:           {
                "P1": PhraseStructure.SENTENCE
            },
            Exposition.P_THEME_ENDING_CADENCE:         Cadence.HC,
            Exposition.TR_THEME_TYPE:                  TRThemeType.DISSOLVING_CONTINUATION,
            Exposition.TR_THEME_MEASURES:              MR(22, 58),
            Exposition.TR_MODULE_MEASURES_DICT:        {
                "TR0":   MR(22, 24),
                "TR1.1": MR(25, 33),
                "TR1.2": MR(33, 44),
                "TR1.3": MR(44, 58),
            },
            Exposition.TR_THEME_OPENING_KEY:           Key.C_MINOR,
            Exposition.TR_THEME_CHROMATIC_PREDOMINANT: False,
            Exposition.TR_THEME_HAMMER_BLOW_COUNT:     2,
            Exposition.TR_THEME_ENERGY:                EnergyChange.ENERGY_GAIN_CRESCENDO,
            Exposition.TR_THEME_DOMINANT_LOCK:         False,
            Exposition.TR_THEME_ENDING_KEY:            Key.EES_MAJOR,
            # Uses A dim7 / C as vii˚7/B-flat
            Exposition.TR_THEME_ENDING_CADENCE:        Cadence.HC_V6,

            Exposition.MC_MEASURES:                    MR(58, 62),
            Exposition.MC_STYLE:                       MC.GENERAL_PAUSE_WITH_S0,

            Exposition.S_THEME_TYPE:                   SThemeType.TRI_MODULAR_S,

            Exposition.S_THEME_MEASURES:               MR(59, 110),
            Exposition.S_MODULE_MEASURES_DICT:         {
                "S0":   MR(59, 62),
                "S1.1": MR(63, 82),
                "S1.2": MR(83, 93),
                "S1.3": MR(94, 110),
            },
            Exposition.S_MODULE_TYPES_DICT:            {
                "S1.1": SThemeType.LYRICAL_CANTABILE,
                "S1.2": SThemeType.OMINOUS_THREATENING,
                "S1.3": SThemeType.HEROIC_CADENTIAL,
            },
            Exposition.S_THEME_OPENING_KEY:            Key.EES_MAJOR,
            Exposition.S_THEME_ENDING_KEY:             Key.EES_MAJOR,
            Exposition.S_THEME_ENDING_CADENCE:         Cadence.PAC_MAJOR,

            Exposition.EEC_ESC_SECURED:                True,
            Exposition.EEC_ESC_MEASURE:                MR(110),

            Exposition.C_THEME_MEASURES_INCL_C_RT:     MR(110, 124),
            Exposition.C_THEME_TYPE:                   CThemeType.FORTE_TR_BASED_C,
            Exposition.C_THEME_OPENING_KEY:            Key.EES_MAJOR,
            Exposition.C_THEME_ENDING_KEY_BEFORE_C_RT: Key.EES_MAJOR,
        }

    @classmethod
    def development_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Development.MEASURES:        MR(125, 248),
            Development.OPENING_KEY:     Key.F_MINOR,
            Development.OTHER_KEYS_LIST: [
                Key.F_MINOR,
                Key.C_MINOR,
                Key.G_MINOR,
                Key.C_MINOR,
                Key.F_MINOR,
            ],
            Development.ENDING_KEY:      Key.C_MINOR,
        }

    @classmethod
    def recapitulation_attribute_dict(cls) -> Dict[Field, Any]:
        recap_dict = cls.exposition_attribute_dict()

        recap_updates = {
            Recapitulation.MEASURES:                        MR(248, 374),

            Recapitulation.P_THEME_MEASURES:                MR(248, 268),
            Recapitulation.P_MODULE_MEASURES_DICT:          {
                "P0":   MR(248, 252),
                "P1.1": MR(253, 261),
                "P1.2": MR(261, 268)
            },
            Recapitulation.P_THEME_TYPE:                    PThemeType.GRAND_ANTECEDENT,
            Recapitulation.P_THEME_CHANGE_FROM_EXPOSITION:  "Oboe has mournful Adagio interlude on final HC",

            Recapitulation.TR_THEME_MEASURES:               MR(269, 302),
            Recapitulation.TR_MODULE_MEASURES_DICT:         {
                "TR1.1": MR(269, 277),
                "TR1.2": MR(277, 288),
                "TR1.3": MR(288, 302),
            },
            Recapitulation.TR_THEME_CHANGE_FROM_EXPOSITION: "TR0 not present. "
                                                            "TR1.3 reaches same C dim chord, but resolves differently",

            Recapitulation.MC_MEASURES:                     MR(302, 306),

            Recapitulation.S_THEME_MEASURES:                MR(303, 362),
            Recapitulation.S_MODULE_MEASURES_DICT:          {
                "S0":   MR(303, 306),
                "S1.1": MR(307, 330),
                "S1.2": MR(331, 345),
                "S1.3": MR(346, 362),
            },
            Recapitulation.S_THEME_OPENING_KEY:             Key.C_MAJOR,
            Recapitulation.S_THEME_ENDING_KEY:              Key.C_MAJOR,
            Recapitulation.EEC_ESC_MEASURE:                 MR(362),

            Recapitulation.C_THEME_MEASURES_INCL_C_RT:      MR(362, 374),
            Recapitulation.C_THEME_OPENING_KEY:             Key.C_MAJOR,
            Recapitulation.C_THEME_ENDING_KEY_BEFORE_C_RT:  Key.C_MAJOR,
            Recapitulation.C_THEME_CHANGE_FROM_EXPOSITION:  "Ending Cadence resolution elided into onset of Coda: "
                                                            "I / C Major = V / F minor"
        }

        recap_dict.update(recap_updates)
        return recap_dict

    @classmethod
    def coda_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Coda.MEASURES:    MR(374, 502),
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
            Sonata.LILYPOND_IMAGE_SETTINGS:  {Sonata.IMAGE_WIDTH: 560}
        }

    @classmethod
    def introduction_attribute_dict(cls) -> Dict[Field, Any]:
        return {}

    @classmethod
    def exposition_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Exposition.MEASURES:                         MR(1, 124),
            Exposition.OPENING_TEMPO:                    "Allegro",

            Exposition.P_THEME_MEASURES:                 MR(1, 26),
            Exposition.P_MODULE_MEASURES_DICT:           {
                "P1.1":    MR(1, 4),
                "P1.2":    MR(5, 12),
                "P1.3":    MR(13, 18),
                "P1.4":    MR(18, 22),
                "P1.5-cf": MR(22, 26),
            },
            Exposition.P_THEME_TYPE:                     PThemeType.GRAND_ANTECEDENT,
            Exposition.P_THEME_OPENING_KEY:              Key.C_MAJOR,
            Exposition.P_THEME_ENDING_KEY:               Key.C_MAJOR,

            Exposition.TR_THEME_MEASURES:                MR(26, 43),
            Exposition.TR_THEME_OPENING_KEY:             Key.C_MAJOR,

            Exposition.TR_THEME_TYPE:                    TRThemeType.INDEPENDENT_SEPARATELY_THEMATIZED,
            Exposition.TR_THEME_COMMENTS:                "Hepokoski calls this dissolving continuation, but I find TR "
                                                         "to have a clearly independent \"new theme\" feel.",
            Exposition.TR_MODULE_PHRASE_DICT:            [PhraseStructure.COMPOUND_SENTENCE],
            Exposition.TR_THEME_CHROMATIC_PREDOMINANT:   False,
            Exposition.TR_THEME_ENERGY:                  EnergyChange.ENERGY_STASIS_FORTE,
            Exposition.TR_THEME_DOMINANT_LOCK:           True,
            Exposition.TR_THEME_ENDING_KEY:              Key.G_MAJOR,
            Exposition.TR_THEME_ENDING_CADENCE:          Cadence.HC,

            Exposition.MC_MEASURES:                      MR(43, 44),
            Exposition.MC_STYLE:                         MC.CAESURA_FILL_CASCADE,

            Exposition.S_THEME_TYPE:                     SThemeType.BUSTLING_GALANT,
            Exposition.S_THEME_MEASURES:                 MR(45, 63),
            # could be 45 if include S headmotive
            Exposition.S_THEME_OPENING_KEY:              Key.G_MAJOR,
            Exposition.S_MODULE_MEASURES_DICT:           {
                "S1.1": MR(45, 58),
                "S1.2": MR(58, 63)
            },
            Exposition.S_THEME_ENDING_KEY:               Key.G_MAJOR,
            Exposition.S_THEME_ENDING_CADENCE:           Cadence.HC,
            Exposition.S_THEME_EVADED_PAC_MEASURES_LIST: [MR(64)],
            Exposition.EEC_ESC_SECURED:                  False,

            Exposition.C_THEME_SC_PRE_EEC_ESC:           True,
            Exposition.C_THEME_MEASURES_INCL_C_RT:       MR(64, 85),
            Exposition.C_MODULE_MEASURES_DICT:           {
                "SC1.1": MR(64, 79),
                "SC1.2": MR(80, 85)
            },
            Exposition.C_THEME_OPENING_KEY:              Key.G_MAJOR,
            Exposition.C_THEME_ENDING_KEY_BEFORE_C_RT:   Key.C_MINOR,
        }

    @classmethod
    def development_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Development.MEASURES:        MR(86, 206),
            Development.OPENING_KEY:     Key.A_MAJOR,
            Development.OTHER_KEYS_LIST: [
                Key.A_MINOR,
                Key.F_MAJOR,
                Key.BES_MAJOR,
                Key.BES_MINOR,
                Key.DES_MAJOR,
                Key.C_MAJOR,
                Key.G_MAJOR,
            ],
            Development.ENDING_KEY:      Key.C_MINOR,

        }

    @classmethod
    def recapitulation_attribute_dict(cls) -> Dict[Field, Any]:
        recap_dict = cls.exposition_attribute_dict_without_fields_unlikely_to_be_same()

        recap_updates = {
            Recapitulation.MEASURES:                       MR(207, 374),

            Recapitulation.P_THEME_MEASURES:               MR(207, 232),
            Recapitulation.P_THEME_TYPE:                   PThemeType.GRAND_ANTECEDENT,
            Exposition.P_MODULE_MEASURES_DICT:             {
                "P1.1":    MR(207, 210),
                "P1.2":    MR(211, 218),
                "P1.3":    MR(219, 224),
                "P1.4":    MR(224, 228),
                "P1.5-cf": MR(228, 232),
            },
            Recapitulation.TR_THEME_MEASURES:              MR(232, 252),
            Recapitulation.TR_THEME_ENDING_KEY:            Key.C_MAJOR,

            Recapitulation.MC_MEASURES:                    MR(252, 253),

            Recapitulation.S_THEME_MEASURES:               MR(254, 272),
            # could be 253 if include S headmotive
            Recapitulation.S_THEME_OPENING_KEY:            Key.C_MAJOR,
            Recapitulation.S_THEME_ENDING_KEY:             Key.C_MAJOR,
            Recapitulation.S_MODULE_MEASURES_DICT:         {
                "S1.1": MR(254, 267),
                "S1.2": MR(267, 272)
            },
            Exposition.S_THEME_EVADED_PAC_MEASURES_LIST:   [MR(273)],
            Recapitulation.EEC_ESC_SECURED:                False,
            Recapitulation.ESC_SUBSTITUTE:                 False,

            Recapitulation.C_THEME_MEASURES_INCL_C_RT:     MR(273, 294),  # or 293 depending on definition
            Recapitulation.C_MODULE_MEASURES_DICT:         {
                "SC1.1":    MR(273, 288),
                "SC1.2var": MR(289, 294)
            },
            Recapitulation.C_THEME_CHANGE_FROM_EXPOSITION: "C1.2 missing bass motives and instead holds C1.1 build-up "
                                                           "static to lead to Coda",

            Recapitulation.C_THEME_OPENING_KEY:            Key.C_MAJOR,
            Recapitulation.C_THEME_ENDING_KEY_BEFORE_C_RT: Key.C_MAJOR,
        }

        recap_dict.update(recap_updates)
        return recap_dict

    @classmethod
    def coda_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Coda.MEASURES:    MR(294, 444),  # could also be 295 if treat S headmotive as not coda
            Coda.OPENING_KEY: Key.C_MAJOR,
            Coda.ENDING_KEY:  Key.C_MAJOR,
        }
