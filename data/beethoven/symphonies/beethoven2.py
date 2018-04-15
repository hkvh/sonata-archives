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
            Introduction.MEASURES:        MR(1, 33),
            Introduction.OPENING_TEMPO:   "Adagio molto",
            Introduction.OPENING_KEY:     Key.D_MAJOR,
            Introduction.OTHER_KEYS_LIST: [
                Key.BES_MAJOR,
                Key.D_MINOR,
            ],
            Introduction.ENDING_KEY:      Key.D_MAJOR,
        }

    @classmethod
    def exposition_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Exposition.MEASURES:                         MR(34, 133),
            Exposition.OPENING_TEMPO:                    "Allegro con brio",

            Exposition.P_THEME_MEASURES:                 MR(34, 57),
            Exposition.P_THEME_PAC_MEASURES_LIST:        [MR(47)],
            Exposition.P_MODULE_PHRASE_DICT:             {
                'P1': PhraseStructure.COMPOUND_SENTENCE,
                'P2': PhraseStructure.HYBRID_1,
            },
            Exposition.P_MODULE_MEASURES_DICT:           {
                'P1': MR(34, 47),
                'P2': MR(47, 57),
            },
            Exposition.P_THEME_TYPE:                     PThemeType.SELF_CONTAINED_PHRASE,
            Exposition.P_THEME_OPENING_KEY:              Key.D_MAJOR,
            Exposition.P_THEME_ENDING_KEY:               Key.D_MINOR,
            Exposition.P_THEME_ENDING_CADENCE:           Cadence.IAC_V6_i,
            Exposition.TR_THEME_MEASURES:                MR(57, 71),
            Exposition.TR_THEME_TYPE:                    TRThemeType.DISSOLVING_RESTATEMENT,
            Exposition.TR_MODULE_TYPES_DICT:             {
                'TR1.1': TRThemeType.DISSOLVING_RESTATEMENT,
                'TR1.2': TRThemeType.SUDDEN_INDEPENDENT_INTERRUPTION,
            },
            Exposition.TR_MODULE_MEASURES_DICT:          {
                'TR1.1': MR(57, 61),
                'TR1.2': MR(61, 71),
            },
            Exposition.TR_THEME_COMMENTS:                "Arguably could start TR with the V / A minor section at m. 61 "
                                                         "(this would match recap V / D minor start at m. 233 which is"
                                                         "the only recap option as m. 57-60 has no corresponding measures) "
                                                         "However, I chose the m. 57 start since it allows the TR to be a "
                                                         "dissolving restatement (which makes more sense due to how "
                                                         "m. 61 is a sudden outburst that seems to interrupt the phrase).",

            Exposition.TR_THEME_OPENING_KEY:             Key.D_MINOR,
            Exposition.TR_THEME_ENERGY:                  EnergyChange.ENERGY_GAIN_CRESCENDO,
            Exposition.TR_THEME_DOMINANT_LOCK:           True,
            Exposition.TR_THEME_CHROMATIC_PREDOMINANT:   False,
            Exposition.TR_THEME_HAMMER_BLOW_COUNT:       0,
            Exposition.TR_THEME_ENDING_KEY:              Key.A_MINOR,
            Exposition.TR_THEME_ENDING_CADENCE:          Cadence.HC,

            Exposition.MC_STYLE:                         MC.CAESURA_FILL_CASCADE,
            Exposition.MC_MEASURES:                      MR(71, 72),
            Exposition.MC_FILL_KEY:                      Key.A_MAJOR,

            Exposition.S_THEME_TYPE:                     SThemeType.MULTI_MODULAR_S,
            Exposition.S_THEME_MEASURES:                 MR(73, 112),
            Exposition.S_THEME_COMMENTS:                 "S1.1 and S1.2 are both Periods where"
                                                         "the consequents end in V:PACs, but these are"
                                                         "not a structural PAC since they are "
                                                         "basically serving as an HC with respect to"
                                                         "the phrase",
            Exposition.S_MODULE_PHRASE_DICT:             {
                'S1.1': PhraseStructure.PERIOD,
                'S1.2': PhraseStructure.PERIOD,
            },
            Exposition.S_MODULE_TYPES_DICT:              {
                'S1.1': SThemeType.BUSTLING_GALANT,
                'S1.2': SThemeType.BUSTLING_GALANT,
                'S1.3': SThemeType.DISASTROUS_FAILED_CADENTIAL,
                'S1.4': [SThemeType.CONTRASTING_P_DERIVATION, SThemeType.RECOVERED_CADENTIAL]
            },
            Exposition.S_MODULE_MEASURES_DICT:           {
                'S1.1': MR(73, 80),
                'S1.2': MR(81, 88),
                'S1.3': MR(88, 101),
                'S1.4': MR(102, 112),
            },

            Exposition.S_THEME_STRONG_PAC_MEASURES_LIST: [MR(80), MR(88)],
            Exposition.S_THEME_EVADED_PAC_MEASURES_LIST: [MR(100)],
            Exposition.S_THEME_OPENING_KEY:              Key.A_MAJOR,
            Exposition.S_THEME_OTHER_KEYS_LIST:          [Key.A_MINOR],
            Exposition.S_THEME_ENDING_KEY:               Key.A_MAJOR,
            Exposition.S_THEME_ENDING_CADENCE:           Cadence.IAC_MAJOR,

            Exposition.EEC_ESC_SECURED:                  True,
            Exposition.EEC_ESC_MEASURE:                  MR(112),
            Exposition.EEC_ESC_COMMENTS:                 "Flute plays soprano 3ˆ, but otherwise feels like strong PAC",

            Exposition.C_THEME_MEASURES_INCL_C_RT:       MR(112, 133),
            Exposition.C_THEME_TYPE:                     CThemeType.FORTE_P_BASED_C,
            Exposition.C_MODULE_MEASURES_DICT:           {
                'C1': MR(112, 131),
            },
            Exposition.C_THEME_OPENING_KEY:              Key.A_MAJOR,
            Exposition.C_THEME_OTHER_KEYS_LIST:          [Key.D_MINOR],
            Exposition.C_THEME_ENDING_KEY_BEFORE_C_RT:   Key.A_MAJOR,
            Exposition.C_RT_PRESENT:                     True,
            Exposition.C_RT_MEASURES:                    MR(132, 133),
            Exposition.C_RT_ENDING_KEY:                  Key.D_MAJOR,
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
            Recapitulation.MEASURES:                         MR(216, 298),

            Recapitulation.P_THEME_MEASURES:                 MR(216, 233),
            Recapitulation.P_THEME_PAC_MEASURES_LIST:        [],
            Recapitulation.P_THEME_ENDING_KEY:               Key.D_MAJOR,
            Recapitulation.P_THEME_ENDING_CADENCE:           Cadence.HC,
            Recapitulation.P_MODULE_PHRASE_DICT:             {
                'P1': PhraseStructure.COMPOUND_SENTENCE,
            },
            Recapitulation.P_MODULE_MEASURES_DICT:           {
                'P1': MR(216, 233),
            },
            Recapitulation.P_THEME_CHANGE_FROM_EXPOSITION:   "P1 ending elongated and P2 elided entirely",

            Recapitulation.TR_THEME_MEASURES:                MR(233, 243),
            Recapitulation.TR_THEME_TYPE:                    TRThemeType.INDEPENDENT_SEPARATELY_THEMATIZED,
            Recapitulation.TR_MODULE_TYPES_DICT:             {
                'TR1.2': TRThemeType.SUDDEN_INDEPENDENT_INTERRUPTION,
            },
            Recapitulation.TR_MODULE_MEASURES_DICT:          {
                'TR1.2': MR(233, 243),
            },
            Recapitulation.TR_THEME_OPENING_KEY:             Key.D_MINOR,
            Recapitulation.TR_THEME_ENDING_KEY:              Key.D_MINOR,
            Recapitulation.TR_THEME_CHANGE_FROM_EXPOSITION:  "TR1.1 elided entirely",
            # If decide to move exposition TR to m. 61, then TR exactly like recap and Expostion P2
            # would be the thing elided

            Recapitulation.MC_MEASURES:                      MR(243, 244),
            Recapitulation.MC_FILL_KEY:                      Key.D_MAJOR,

            Recapitulation.S_THEME_MEASURES:                 MR(245, 284),
            Recapitulation.S_MODULE_MEASURES_DICT:           {
                'S1.1': MR(245, 252),
                'S1.2': MR(253, 260),
                'S1.3': MR(260, 273),
                'S1.4': MR(274, 284),
            },
            Recapitulation.S_THEME_STRONG_PAC_MEASURES_LIST: [MR(252), MR(260)],
            Recapitulation.S_THEME_EVADED_PAC_MEASURES_LIST: [MR(272)],
            Recapitulation.S_THEME_OPENING_KEY:              Key.D_MAJOR,
            Recapitulation.S_THEME_OTHER_KEYS_LIST:          [Key.D_MINOR],
            Recapitulation.S_THEME_ENDING_KEY:               Key.D_MAJOR,
            Exposition.EEC_ESC_MEASURE:                      MR(284),

            Recapitulation.C_THEME_MEASURES_INCL_C_RT:       MR(284, 305),
            Recapitulation.C_MODULE_MEASURES_DICT:           {
                'C1': MR(284, 303),
            },
            Recapitulation.C_THEME_OPENING_KEY:              Key.D_MAJOR,
            Recapitulation.C_THEME_OTHER_KEYS_LIST:          [Key.G_MINOR],
            Recapitulation.C_THEME_ENDING_KEY_BEFORE_C_RT:   Key.D_MAJOR,

            Recapitulation.C_RT_MEASURES:                    MR(304, 305),
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
