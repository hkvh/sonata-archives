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
            Expo.MEASURES:                 MR(1, 124),
            Expo.OPENING_TEMPO:            "Allegro con brio",

            Expo.P_MEASURES:               MR(1, 21),
            Expo.P_OPENING_KEY:            Key.C_MINOR,
            Expo.P_TYPE:                   PThemeType.GRAND_ANTECEDENT,
            Expo.P_MODULE_MEASURES_DICT:   {
                "P0":   MR(1, 5),
                "P1.1": MR(6, 14),
                "P1.2": MR(14, 21)
            },
            Expo.P_COMMENTS:               "I am calling mm. 1-5 P0 since it is an opening motto that is "
                                           "cordoned off from the rest of P1, "
                                           "but it is a somewhat unusual P0 case since P1.1 "
                                           "is obviously completely derived from P0. "
                                           "(Hepokoski calls it P1.0 which is also defensible)",
            Expo.P_MODULE_PHRASE_DICT:     {
                "P1": PhraseStructure.SENTENCE
            },
            Expo.P_MODULE_TYPES_DICT:      {
                "P0": PThemeType.OPENING_MOTTO,
                "P1": PThemeType.GRAND_ANTECEDENT,
            },
            Expo.P_ENDING_KEY:             Key.C_MINOR,
            Expo.P_ENDING_CADENCE:         Cadence.HC,
            Expo.TR_TYPE:                  TRThemeType.DISSOLVING_CONTINUATION,
            Expo.TR_MEASURES:              MR(22, 58),
            Expo.TR_MODULE_MEASURES_DICT:  {
                "TR0":   MR(22, 24),
                "TR1.1": MR(25, 33),
                "TR1.2": MR(33, 44),
                "TR1.3": MR(44, 58),
            },
            Expo.TR_COMMENTS:              "Even though TR1.2 is an Independent Developmental module, "
                                           "I am not considering the overall type to be a Multi-Modular "
                                           "or Mixed TR because the net effect is that of the Dissolving "
                                           "Continuation TR",
            Expo.TR_MODULE_TYPES_DICT:     {
                "TR0":   TRThemeType.OPENING_MOTTO,
                "TR1.1": TRThemeType.DISSOLVING_CONTINUATION,
                "TR1.2": TRThemeType.INDEPENDENT_DEVELOPMENTAL,
                "TR1.3": TRThemeType.DISSOLVING_CONTINUATION,
            },
            Expo.TR_OPENING_KEY:           Key.C_MINOR,
            Expo.TR_CHROM_PREDOM:          False,
            Expo.TR_HAMMER_COUNT:          2,
            Expo.TR_ENERGY:                EnergyChange.ENERGY_GAIN_CRESCENDO,
            Expo.TR_DOMINANT_LOCK:         False,
            Expo.TR_ENDING_KEY:            Key.EES_MAJOR,
            # Uses A dim7 / C as vii˚7/B-flat
            Expo.TR_ENDING_CADENCE:        Cadence.HC_V6,

            Expo.MC_MEASURES:              MR(58, 62),
            Expo.MC_STYLE:                 MC.GENERAL_PAUSE_WITH_S0,

            Expo.S_TYPE:                   SThemeType.TRI_MODULAR_S,

            Expo.S_MEASURES:               MR(59, 110),
            Expo.S_MODULE_MEASURES_DICT:   {
                "S0":   MR(59, 62),
                "S1.1": MR(63, 82),
                "S1.2": MR(83, 93),
                "S1.3": MR(94, 110),
            },
            Expo.S_MODULE_TYPES_DICT:      {
                "S0":   SThemeType.OPENING_MOTTO,
                "S1.1": SThemeType.LYRICAL_CANTABILE,
                "S1.2": SThemeType.OMINOUS_THREATENING,
                "S1.3": SThemeType.HEROIC_CADENTIAL,
            },
            Expo.S_STRONG_PAC_MEAS_LIST:   [MR(110)],
            Expo.S_OPENING_KEY:            Key.EES_MAJOR,
            Expo.S_ENDING_KEY:             Key.EES_MAJOR,
            Expo.S_ENDING_CADENCE:         Cadence.PAC_MAJOR,

            Expo.EEC_ESC_SECURED:          True,
            Expo.EEC_ESC_MEASURE:          MR(110),

            Expo.C_MEASURES_INCL_C_RT:     MR(110, 124),
            Expo.C_TYPE:                   CThemeType.FORTE_TR_BASED_C,
            Expo.C_MODULE_MEASURES_DICT:   {
                'C1': MR(110, 124)
            },
            Expo.C_PAC_MEASURES_LIST:      [MR(122)],
            Expo.C_OPENING_KEY:            Key.EES_MAJOR,
            Expo.C_ENDING_KEY_BEFORE_C_RT: Key.EES_MAJOR,
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
        recap_dict = cls.exposition_attribute_dict_without_fields_unlikely_to_be_same()

        recap_updates = {
            Recap.MEASURES:                 MR(248, 374),

            Recap.P_MEASURES:               MR(248, 268),
            Recap.P_MODULE_MEASURES_DICT:   {
                "P0":   MR(248, 252),
                "P1.1": MR(253, 261),
                "P1.2": MR(261, 268)
            },
            Recap.P_TYPE:                   PThemeType.GRAND_ANTECEDENT,
            Recap.P_COMMENTS:               "Oboe has mournful Adagio interlude on final HC",

            Recap.TR_MEASURES:              MR(269, 302),
            Recap.TR_MODULE_MEASURES_DICT:  {
                "TR1.1": MR(269, 277),
                "TR1.2": MR(277, 288),
                "TR1.3": MR(288, 302),
            },
            Expo.TR_MODULE_TYPES_DICT:      {
                "TR1.1": TRThemeType.DISSOLVING_CONTINUATION,
                "TR1.2": TRThemeType.INDEPENDENT_DEVELOPMENTAL,
                "TR1.3": TRThemeType.DISSOLVING_CONTINUATION,
            },
            Recap.TR_ENDING_KEY:            Key.C_MAJOR,
            Recap.TR_COMMENTS:              "TR0 opening motto not present. "
                                            "TR1.3 reaches same C dim chord, but resolves differently",

            Recap.MC_MEASURES:              MR(302, 306),

            Recap.S_MEASURES:               MR(303, 362),
            Recap.S_MODULE_MEASURES_DICT:   {
                "S0":   MR(303, 306),
                "S1.1": MR(307, 330),
                "S1.2": MR(331, 345),
                "S1.3": MR(346, 362),
            },
            Recap.S_OPENING_KEY:            Key.C_MAJOR,
            Recap.S_ENDING_KEY:             Key.C_MAJOR,
            Recap.S_STRONG_PAC_MEAS_LIST:   [MR(362)],
            Recap.S_COMMENTS:               "S0 is played by bassoons instead of horns",
            Recap.EEC_ESC_MEASURE:          MR(362),

            Recap.C_MEASURES_INCL_C_RT:     MR(362, 374),
            Recap.C_MODULE_MEASURES_DICT:   {
                'C1': MR(362, 374)
            },
            Recap.C_OPENING_KEY:            Key.C_MAJOR,
            Recap.C_ENDING_KEY_BEFORE_C_RT: Key.C_MAJOR,
            Recap.C_PAC_MEASURES_LIST:      [MR(374)],
            Recap.C_COMMENTS:               "Ending PAC resolution of C Major C elided into onset of Coda: "
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
            Expo.MEASURES:                 MR(1, 124),
            Expo.OPENING_TEMPO:            "Allegro",

            Expo.P_MEASURES:               MR(1, 26),
            Expo.P_MODULE_MEASURES_DICT:   {
                "P1.1":    MR(1, 4),
                "P1.2":    MR(5, 12),
                "P1.3":    MR(13, 18),
                "P1.4":    MR(18, 22),
                "P1.5-cf": MR(22, 26),
            },
            Expo.P_TYPE:                   PThemeType.GRAND_ANTECEDENT,
            Expo.P_OPENING_KEY:            Key.C_MAJOR,
            Expo.P_ENDING_KEY:             Key.C_MAJOR,
            Expo.P_ENDING_CADENCE:         Cadence.HC,
            Expo.P_COMMENTS:               "In m. 22, P ends with an unusual I: HC caesura fill module (P1.5cf) "
                                           "that is somewhat in dialogue with an MC effect, but what follows "
                                           "in m. 26 is clearly the onset of"
                                           "TR, and thus m. 22 is not a real candidate to be an MC",

            Expo.TR_MEASURES:              MR(26, 43),
            Recap.TR_MODULE_MEASURES_DICT: {
                "TR1": MR(26, 43)
            },
            Expo.TR_OPENING_KEY:           Key.C_MAJOR,

            Expo.TR_TYPE:                  TRThemeType.INDEPENDENT_SEPARATELY_THEMATIZED,
            Expo.TR_COMMENTS:              "Hepokoski calls this dissolving continuation, but I find TR "
                                           "to have a clearly independent \"new theme\" feel.",
            Expo.TR_MODULE_PHRASE_DICT:    [PhraseStructure.COMPOUND_SENTENCE],
            Expo.TR_CHROM_PREDOM:          False,
            Expo.TR_ENERGY:                EnergyChange.ENERGY_STASIS_FORTE,
            Expo.TR_DOMINANT_LOCK:         True,
            Expo.TR_ENDING_KEY:            Key.G_MAJOR,
            Expo.TR_ENDING_CADENCE:        Cadence.HC,
            Expo.TR_HAMMER_COUNT:          0,

            Expo.MC_MEASURES:              MR(43, 44),
            Expo.MC_STYLE:                 MC.CAESURA_FILL_CASCADE,

            Expo.S_TYPE:                   SThemeType.MULTI_MODULAR_S,
            Expo.S_MEASURES:               MR(45, 63),
            # could be 45 if include S headmotive
            Expo.S_OPENING_KEY:            Key.G_MAJOR,
            Expo.S_MODULE_MEASURES_DICT:   {
                "S1.1": MR(45, 58),
                "S1.2": MR(58, 63)
            },
            Expo.S_MODULE_TYPES_DICT:      {
                "S1.1": SThemeType.FORTE_PIANO_ALTERNATING,
                "S1.2": SThemeType.BUSTLING_GALANT,
            },
            Expo.S_ENDING_KEY:             Key.G_MAJOR,
            Expo.S_ENDING_CADENCE:         Cadence.HC,
            Expo.S_EVADED_PAC_MEAS_LIST:   [MR(64)],
            Expo.EEC_ESC_SECURED:          False,

            Expo.C_SC_PRE_EEC_ESC:         True,
            Expo.C_TYPE:                   CThemeType.S_C_PRE_EEC,
            Expo.C_MEASURES_INCL_C_RT:     MR(64, 85),
            Expo.C_MODULE_MEASURES_DICT:   {
                "SC1.1": MR(64, 79),
                "SC1.2": MR(80, 85)
            },
            Expo.C_MODULE_TYPES_DICT:      {
                "SC1.1": CThemeType.NEW_THEME_C,
                "SC1.2": CThemeType.FURIOUS_BUILDUP,
            },
            Expo.C_OPENING_KEY:            Key.G_MAJOR,
            Expo.C_ENDING_KEY_BEFORE_C_RT: Key.C_MINOR,
            Expo.C_COMMENTS:               "The C section I'm starting at m. 64 is not actually C "
                                           "because there is no EEC "
                                           "which is why I'm using the sonata theory"
                                           "label S^C (pre-EEC) to describe it. "
                                           "It is somewhat of a debatable use of the label as it is not "
                                           "especially in dialogue with C1 logic at m. 62, so it might "
                                           "be classified as S1.3 and S1.4 instead of SC1.1 and SC1.2. "
                                           "However, I do think there is an intrinsic closing-theme"
                                           "feel to this theme by m. 72 though, which is why I stand by "
                                           "the S^C label for now."
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
            Recap.MEASURES:                 MR(207, 374),

            Recap.P_MEASURES:               MR(207, 232),
            Recap.P_TYPE:                   PThemeType.GRAND_ANTECEDENT,
            Recap.P_MODULE_MEASURES_DICT:   {
                "P1.1":    MR(207, 210),
                "P1.2":    MR(211, 218),
                "P1.3":    MR(219, 224),
                "P1.4":    MR(224, 228),
                "P1.5-cf": MR(228, 232),
            },

            Recap.TR_MEASURES:              MR(232, 252),
            Recap.TR_MODULE_MEASURES_DICT:  {
                "TR1": MR(232, 252)
            },
            Recap.TR_ENDING_KEY:            Key.C_MAJOR,

            Recap.MC_MEASURES:              MR(252, 253),

            Recap.S_MEASURES:               MR(254, 272),
            # could be 253 if include S headmotive
            Recap.S_OPENING_KEY:            Key.C_MAJOR,
            Recap.S_ENDING_KEY:             Key.C_MAJOR,
            Recap.S_MODULE_MEASURES_DICT:   {
                "S1.1": MR(254, 267),
                "S1.2": MR(267, 272)
            },
            Expo.S_EVADED_PAC_MEAS_LIST:    [MR(273)],
            Recap.EEC_ESC_SECURED:          False,
            Recap.ESC_FALSE_SUBSTITUTE:     False,

            Recap.C_MEASURES_INCL_C_RT:     MR(273, 294),  # or 293 depending on definition
            Recap.C_MODULE_MEASURES_DICT:   {
                "SC1.1":    MR(273, 288),
                "SC1.2var": MR(289, 294)
            },
            Recap.C_COMMENTS:               "C1.2 missing bass motives and instead holds C1.1 build-up "
                                            "static to lead to Coda",

            Recap.C_OPENING_KEY:            Key.C_MAJOR,
            Recap.C_ENDING_KEY_BEFORE_C_RT: Key.C_MAJOR,
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
