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
            Sonata.LILYPOND_IMAGE_SETTINGS:  {Sonata.IMAGE_WIDTH: 600}
        }

    @classmethod
    def introduction_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Intro.MEASURES:        MR(1, 33),
            Intro.OPENING_TEMPO:   "Adagio molto",
            Intro.OPENING_KEY:     Key.D_MAJOR,
            Intro.OTHER_KEYS_LIST: [
                Key.BES_MAJOR,
                Key.D_MINOR,
            ],
            Intro.ENDING_KEY:      Key.D_MAJOR,
        }

    @classmethod
    def exposition_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Expo.MEASURES:                 MR(34, 133),
            Expo.OPENING_TEMPO:            "Allegro con brio",

            Expo.P_MEASURES:               MR(34, 57),
            Expo.P_PAC_MEASURES_LIST:      [MR(47)],
            Expo.P_MODULE_PHRASE_DICT:     {
                'P1': PhraseStructure.COMPOUND_SENTENCE,
                'P2': PhraseStructure.HYBRID_1,
            },
            Expo.P_MODULE_MEASURES_DICT:   {
                'P1': MR(34, 47),
                'P2': MR(47, 57),
            },
            Expo.P_TYPE:                   PThemeType.SELF_CONTAINED_PHRASE,
            Expo.P_OPENING_KEY:            Key.D_MAJOR,
            Expo.P_ENDING_KEY:             Key.D_MINOR,
            Expo.P_ENDING_CADENCE:         Cadence.IAC_V6_i,
            Expo.TR_MEASURES:              MR(57, 71),
            Expo.TR_TYPE:                  TRThemeType.DISSOLVING_RESTATEMENT,
            Expo.TR_MODULE_TYPES_DICT:     {
                'TR1.1': TRThemeType.DISSOLVING_RESTATEMENT,
                'TR1.2': TRThemeType.SUDDEN_INDEPENDENT_INTERRUPTION,
            },
            Expo.TR_MODULE_MEASURES_DICT:  {
                'TR1.1': MR(57, 61),
                'TR1.2': MR(61, 71),
            },
            Expo.TR_COMMENTS:              "Arguably could start TR with the V / A minor section at m. 61 "
                                           "(this would match recap V / D minor start at m. 233 which is"
                                           "the only recap option as m. 57-60 has no corresponding measures) "
                                           "However, I chose the m. 57 start since it allows the TR to be a "
                                           "dissolving restatement (which makes more sense due to how "
                                           "m. 61 is a sudden outburst that seems to interrupt the phrase).",

            Expo.TR_OPENING_KEY:           Key.D_MINOR,
            Expo.TR_ENERGY:                EnergyChange.ENERGY_GAIN_CRESCENDO,
            Expo.TR_DOMINANT_LOCK:         True,
            Expo.TR_CHROM_PREDOM:          False,
            Expo.TR_HAMMER_COUNT:          0,
            Expo.TR_ENDING_KEY:            Key.A_MINOR,
            Expo.TR_ENDING_CADENCE:        Cadence.HC,

            Expo.MC_STYLE:                 MC.CAESURA_FILL_CASCADE,
            Expo.MC_MEASURES:              MR(71, 72),
            Expo.MC_FILL_KEY:              Key.A_MAJOR,

            Expo.S_TYPE:                   SThemeType.MULTI_MODULAR_S,
            Expo.S_MEASURES:               MR(73, 112),
            Expo.S_COMMENTS:               "S1.1 and S1.2 are both Periods where"
                                           "the consequents end in V:PACs, but these are"
                                           "not a structural PAC since they are "
                                           "basically serving as an HC with respect to"
                                           "the phrase",
            Expo.S_MODULE_PHRASE_DICT:     {
                'S1.1': PhraseStructure.PERIOD,
                'S1.2': PhraseStructure.PERIOD,
            },
            Expo.S_MODULE_TYPES_DICT:      {
                'S1.1': SThemeType.BUSTLING_GALANT,
                'S1.2': SThemeType.BUSTLING_GALANT,
                'S1.3': SThemeType.DISASTROUS_FAILED_CADENTIAL,
                'S1.4': [SThemeType.CONTRASTING_P_DERIVATION, SThemeType.RECOVERED_CADENTIAL]
            },
            Expo.S_MODULE_MEASURES_DICT:   {
                'S1.1': MR(73, 80),
                'S1.2': MR(81, 88),
                'S1.3': MR(88, 101),
                'S1.4': MR(102, 112),
            },

            Expo.S_STRONG_PAC_MEAS_LIST:   [MR(80), MR(88)],
            Expo.S_ATTEN_PAC_MEAS_LIST:    [MR(112)],
            Expo.S_EVADED_PAC_MEAS_LIST:   [MR(100)],
            Expo.S_OPENING_KEY:            Key.A_MAJOR,
            Expo.S_OTHER_KEYS_LIST:        [Key.A_MINOR],
            Expo.S_ENDING_KEY:             Key.A_MAJOR,
            Expo.S_ENDING_CADENCE:         Cadence.IAC_MAJOR,

            Expo.EEC_ESC_SECURED:          True,
            Expo.EEC_ESC_MEASURE:          MR(112),
            Expo.EEC_ESC_COMMENTS:         "Flute plays soprano 3ˆ in highest register, but otherwise "
                                           "it feels like a strong PAC, despite technically being an IAC."
                                           "(Violin I trill-cadence resolves to high 1^) "
                                           "I will thus consider it to be a type of PAC "
                                           "that does properly secure the EEC, with the flute cover tone "
                                           "serving as mild attenuation",

            Expo.C_MEASURES_INCL_C_RT:     MR(112, 133),
            Expo.C_TYPE:                   CThemeType.FORTE_P_BASED_C,
            Expo.C_MODULE_MEASURES_DICT:   {
                'C1': MR(112, 131),
            },
            Expo.C_OPENING_KEY:            Key.A_MAJOR,
            Expo.C_OTHER_KEYS_LIST:        [Key.D_MINOR],
            Expo.C_ENDING_KEY_BEFORE_C_RT: Key.A_MAJOR,
            Expo.C_RT_PRESENT:             True,
            Expo.C_RT_MEASURES:            MR(132, 133),
            Expo.C_RT_ENDING_KEY:          Key.D_MAJOR,
        }

    @classmethod
    def development_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Development.MEASURES:       MR(134, 216),
            Development.OPENING_KEY:    Key.D_MINOR,
            Development.ENDING_KEY:     Key.D_MAJOR,
            Development.ENDING_CADENCE: Cadence.PAC_MAJOR

        }

    @classmethod
    def recapitulation_attribute_dict(cls) -> Dict[Field, Any]:
        recap_dict = cls.exposition_attribute_dict_without_fields_unlikely_to_be_same()

        recap_updates = {
            Recap.MEASURES:                 MR(216, 298),

            Recap.P_MEASURES:               MR(216, 233),
            Recap.P_PAC_MEASURES_LIST:      [],
            Recap.P_ENDING_KEY:             Key.D_MAJOR,
            Recap.P_ENDING_CADENCE:         Cadence.HC,
            Recap.P_MODULE_PHRASE_DICT:     {
                'P1': PhraseStructure.COMPOUND_SENTENCE,
            },
            Recap.P_MODULE_MEASURES_DICT:   {
                'P1': MR(216, 233),
            },
            Recap.P_COMMENTS:               "P1 ending elongated and P2 elided entirely",

            Recap.TR_MEASURES:              MR(233, 243),
            Recap.TR_TYPE:                  TRThemeType.INDEPENDENT_SEPARATELY_THEMATIZED,
            Recap.TR_MODULE_TYPES_DICT:     {
                'TR1.2': TRThemeType.SUDDEN_INDEPENDENT_INTERRUPTION,
            },
            Recap.TR_MODULE_MEASURES_DICT:  {
                'TR1.2': MR(233, 243),
            },
            Recap.TR_OPENING_KEY:           Key.D_MINOR,
            Recap.TR_ENDING_KEY:            Key.D_MINOR,
            Recap.TR_COMMENTS:              "TR1.1 elided entirely",
            # If decide to move exposition TR to m. 61, then TR exactly like recap and Expostion P2
            # would be the thing elided

            Recap.MC_MEASURES:              MR(243, 244),
            Recap.MC_FILL_KEY:              Key.D_MAJOR,

            Recap.S_MEASURES:               MR(245, 284),
            Recap.S_MODULE_MEASURES_DICT:   {
                'S1.1': MR(245, 252),
                'S1.2': MR(253, 260),
                'S1.3': MR(260, 273),
                'S1.4': MR(274, 284),
            },
            Recap.S_STRONG_PAC_MEAS_LIST:   [MR(252), MR(260)],
            Recap.S_ATTEN_PAC_MEAS_LIST:    [MR(284)],
            Recap.S_EVADED_PAC_MEAS_LIST:   [MR(272)],
            Recap.S_OPENING_KEY:            Key.D_MAJOR,
            Recap.S_OTHER_KEYS_LIST:        [Key.D_MINOR],
            Recap.S_ENDING_KEY:             Key.D_MAJOR,
            Expo.EEC_ESC_MEASURE:           MR(284),

            Recap.C_MEASURES_INCL_C_RT:     MR(284, 305),
            Recap.C_MODULE_MEASURES_DICT:   {
                'C1': MR(284, 303),
            },
            Recap.C_OPENING_KEY:            Key.D_MAJOR,
            Recap.C_OTHER_KEYS_LIST:        [Key.G_MINOR],
            Recap.C_ENDING_KEY_BEFORE_C_RT: Key.D_MAJOR,

            Recap.C_RT_MEASURES:            MR(304, 305),
        }

        recap_dict.update(recap_updates)
        return recap_dict

    @classmethod
    def coda_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Coda.MEASURES:    MR(306, 360),
            Coda.OPENING_KEY: Key.G_MAJOR,
            Coda.ENDING_KEY:  Key.D_MAJOR,
        }
