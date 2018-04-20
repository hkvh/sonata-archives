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

class Beethoven4(PieceDataClass):
    @classmethod
    def piece_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Piece.ID:             "beethoven4",
            Piece.COMPOSER_ID:    Beethoven.id(),
            Piece.NAME:           "Symphony No. 4",
            Piece.CATALOGUE_ID:   "Op. 60",
            Piece.GLOBAL_KEY:     Key.BES_MAJOR,
            Piece.YEAR_STARTED:   1806,
            Piece.YEAR_COMPLETED: 1806,
            Piece.NUM_MOVEMENTS:  4,
            Piece.PIECE_TYPE:     PieceType.SYMPHONY
        }


#################
# Sonata(s)
#################

class Beethoven4_1(SonataDataClass):
    @classmethod
    def sonata_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Sonata.PIECE_ID:                 Beethoven4.id(),
            Sonata.MOVEMENT_NUM:             1,
            Sonata.SONATA_TYPE:              SonataType.TYPE_3,
            Sonata.GLOBAL_KEY:               Key.BES_MAJOR,
            Sonata.MEASURE_COUNT:            498,
            Sonata.INTRODUCTION_PRESENT:     True,
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
            Intro.COMMENTS:                  """
Determining end of Introduction is tricky...

P1.1 starts at m. 43 (so it's definitely over by then) while the Allegro starts at m. 39.
But the quasi-P1.0 motive that starts in m. 36 also happens in exposition first ending –
the last 12 (un-numbered) first ending measures map exactly to m. 36-44:
    m. 36-38 are augmented to 6 measures to make up for doubly-fast tempo and
    m. 39-44 happen almost identically.
But, complicating things, the recap omits m. 36-40 and only contains the P1.0 diminution thing from m. 41-42.

It is thus credible to make m. 36 or m. 40 be the start of the exposition with P1.0, but I'll just
for now bypass this question entirely by making all the P1.0 stuff considered exposition
wind-up (which is what Hepokoski seems to endorse), and start the exposition with P1.1 in m. 43. 
However, the fact that the first ending and recap play this wind-up as quasi-P1.0 does bother me a bit...
            """,
            Intro.MEASURES:                  MR(1, 42),
            Intro.OPENING_TEMPO:             "Adagio",
            Intro.OPENING_KEY:               Key.BES_MINOR,
            Intro.EXPOSITION_WINDUP:         True,
            Intro.EXPOSITION_WINDUP_MEASURE: MR(35),
            Intro.ENDING_KEY:                Key.BES_MAJOR,
        }

    @classmethod
    def exposition_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            # See discussion above: m. 36, m. 49 or m. 41 are all credible starts if want to include
            # wind-up as P1.0, but for now I will not have and P1.0
            Expo.MEASURES:                 MR(43, 187),
            Expo.COMMENTS:                 "Wind-up could alternatively be considered P1.0, "
                                           "meaning the start could be m. 36, 39 or 41",

            Expo.OPENING_TEMPO:            "Allegro con brio",

            Expo.P_MEASURES:               MR(43, 81),
            Expo.P_TYPE:                   PThemeType.ABORTED_ROUNDED_BINARY,
            Expo.P_MODULE_MEASURES_DICT:   {
                "P1":   MR(43, 65),
                "P2.1": MR(65, 81),
            },
            Expo.P_MODULE_PHRASE_DICT:     {
                "P1": PhraseStructure.PERIOD,
            },
            Expo.P_OPENING_KEY:            Key.BES_MAJOR,
            Expo.P_ENDING_KEY:             Key.BES_MAJOR,
            Expo.P_ENDING_CADENCE:         Cadence.IAC_TONIC_BASS_PEDAL,
            Expo.P_PAC_MEASURES_LIST:      [MR(65)],

            Expo.TR_MEASURES:              MR(81, 103),
            Expo.TR_TYPE:                  TRThemeType.DISSOLVING_REPRISE,
            Expo.TR_MODULE_MEASURES_DICT:  {
                "TR1.1": MR(81, 95),
                "TR1.2": MR(95, 103),
            },
            Expo.TR_OPENING_KEY:           Key.BES_MAJOR,
            Expo.TR_ENERGY:                EnergyChange.ENERGY_STASIS_FORTE,
            Expo.TR_HAMMER_COUNT:          0,
            Expo.TR_CHROM_PREDOM:          True,
            Expo.TR_ENDING_KEY:            Key.F_MINOR,
            Expo.TR_ENDING_CADENCE:        Cadence.HC,

            Expo.MC_MEASURES:              MR(103, 106),
            Expo.MC_STYLE:                 MC.CAESURA_FILL_CASCADE,
            Expo.MC_FILL_KEY:              Key.F_MAJOR,

            Expo.S_MEASURES:               MR(107, 177),
            Expo.S_TYPE:                   SThemeType.MULTI_MODULAR_S,
            Expo.S_MODULE_MEASURES_DICT:   {
                "S1.1": MR(107, 112),
                "S1.2": MR(113, 120),
                "S1.3": MR(121, 134),
                "S1.4": MR(135, 141),
                "S2.1": MR(141, 158),
                "S2.2": MR(159, 177)
            },
            Expo.S_OPENING_KEY:            Key.F_MAJOR,
            Expo.S_OTHER_KEYS_LIST:        [
                Key.D_MINOR,
            ],
            Expo.S_ENDING_KEY:             Key.BES_MAJOR,
            Expo.S_STRONG_PAC_MEAS_LIST:   [MR(177)],
            Expo.S_ATTEN_PAC_MEAS_LIST:    [MR(141)],
            Expo.S_EVADED_PAC_MEAS_LIST:   [MR(163), MR(167)],
            Expo.S_ENDING_CADENCE:         Cadence.PAC_MAJOR,

            Expo.EEC_ESC_SECURED:          True,
            Expo.EEC_ESC_MEASURE:          MR(177),

            Expo.C_MEASURES_INCL_C_RT:     MR(177, 187),
            Expo.C_TYPE:                   CThemeType.FORTE_P_DERIVATION_C,
            Expo.C_MODULE_MEASURES_DICT:   {
                'C1': MR(177, 187)
            },
            Expo.C_COMMENTS:               "Could maybe consider m. 141 EEC and S2 as C0 but the m. 141 "
                                           "cadence is attenuated, and the S2.1 motives after m. 141 "
                                           "link back to diminution of bass cadential 1.4 motives "
                                           "in m. 135-140. Also, C-RT is in first ending which has"
                                           "no measure numbers since not present in second ending.",
            Expo.C_OPENING_KEY:            Key.F_MAJOR,
            Expo.C_ENDING_KEY_BEFORE_C_RT: Key.F_MAJOR,
            Expo.C_RT_PRESENT:             True,
            Expo.C_RT_ENDING_KEY:          Key.BES_MAJOR,
        }

    @classmethod
    def development_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Development.MEASURES:        MR(187, 336),
            Development.OPENING_KEY:     Key.F_MAJOR,
            Development.OTHER_KEYS_LIST: [
                Key.D_MAJOR,
                Key.G_MINOR,
                Key.EES_MAJOR,
                Key.C_MAJOR,
                Key.B_MAJOR,
            ],
            Development.ENDING_KEY:      Key.BES_MAJOR,
        }

    @classmethod
    def recapitulation_attribute_dict(cls) -> Dict[Field, Any]:
        recap_dict = cls.exposition_attribute_dict_without_fields_unlikely_to_be_same()

        recap_updates = {
            Recap.COMMENTS:                 "If include wind-up as P0, recap could begin in "
                                            "m. 347 (especially since tonic starts there)",
            Recap.MEASURES:                 MR(337, 461),

            Recap.P_MEASURES:               MR(337, 351),
            Recap.P_MODULE_MEASURES_DICT:   {
                "P1": MR(337, 351),
            },
            Recap.P_MODULE_PHRASE_DICT:     {
                "P1": PhraseStructure.ANTECEDENT,
            },
            Recap.P_COMMENTS:               "P1 vastly truncated (no consequent) and "
                                            "P2 absent entirely",
            Recap.TR_MEASURES:              MR(351, 377),
            Recap.TR_MODULE_MEASURES_DICT:  {
                "TR1.1": MR(351, 369),
                "TR1.2": MR(369, 377),
            },
            Recap.TR_ENDING_KEY:            Key.BES_MAJOR,

            Recap.MC_MEASURES:              MR(377, 380),

            Recap.S_MEASURES:               MR(381, 451),
            Recap.S_MODULE_MEASURES_DICT:   {
                "S1.1": MR(381, 386),
                "S1.2": MR(387, 394),
                "S1.3": MR(395, 408),
                "S1.4": MR(409, 415),
                "S2.1": MR(415, 432),
                "S2.2": MR(433, 451)
            },
            Recap.S_OPENING_KEY:            Key.BES_MAJOR,
            Recap.S_STRONG_PAC_MEAS_LIST:   [MR(451)],
            Recap.S_ATTEN_PAC_MEAS_LIST:    [MR(415)],
            Recap.S_EVADED_PAC_MEAS_LIST:   [MR(437), MR(441)],
            Recap.S_ENDING_KEY:             Key.BES_MAJOR,
            Recap.EEC_ESC_MEASURE:          MR(451),

            Recap.C_MEASURES_INCL_C_RT:     MR(451, 461),
            Recap.C_MODULE_MEASURES_DICT:   {
                "C1": MR(451, 461),
            },
            Recap.C_OPENING_KEY:            Key.BES_MAJOR,
            Recap.C_ENDING_KEY_BEFORE_C_RT: Key.BES_MAJOR,
            Recap.C_RT_PRESENT:             False,
        }

        recap_dict.update(recap_updates)
        return recap_dict

    @classmethod
    def coda_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Coda.MEASURES:    MR(461, 498),
            Coda.P_RECALLED:  True,
            Coda.OPENING_KEY: Key.BES_MAJOR,
            Coda.ENDING_KEY:  Key.BES_MAJOR,
        }
