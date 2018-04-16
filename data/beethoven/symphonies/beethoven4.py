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
            # Determining end of Introduction is tricky...

            # P1.1 starts at m. 43 (so it's definitely over by then)
            # Allegro starts at m. 39
            # But the quasi-P1.0 motive that starts in m. 36 also happens in exposition first ending
            # First ending's last 12 measures map exactly to m. 36-44:
            #    m. 36-38 are augmented to 6 measures to make up for doubly-fast tempo
            #    m. 39-44 happen almost identically
            # But the recap omits m. 36-40 and only contains the P1.0 diminution thing in m. 41-42

            # It is thus credible to make m. 36 or m. 40 be the start of the exposition, but I'll just
            # for now bypass this question entirely by making all the P1.0 stuff considered exposition
            # wind-up (which is what Hepokoski himself implies in Elements of Sonata Theory), but
            # I am noting that the fact the first ending and recap play this stuff does bother me a bit
            Introduction.MEASURES:                  MR(1, 42),
            Introduction.OPENING_TEMPO:             "Adagio",
            Introduction.OPENING_KEY:               Key.BES_MINOR,
            Introduction.EXPOSITION_WINDUP:         True,
            Introduction.EXPOSITION_WINDUP_MEASURE: MR(35),
            Introduction.ENDING_KEY:                Key.BES_MAJOR,
        }

    @classmethod
    def exposition_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            # See discussion above: m. 36, m. 49 or m. 41 are all credible starts if want to include
            # wind-up as P1.0, but for now I will not have and P1.0
            Exposition.MEASURES:                         MR(43, 187),
            Exposition.COMMENTS:                         "Wind-up could alternatively be considered P1.0, "
                                                         "meaning the start could be m. 36, 39 or 41",

            Exposition.OPENING_TEMPO:                    "Allegro con brio",

            Exposition.P_THEME_MEASURES:                 MR(43, 81),
            Exposition.P_THEME_TYPE:                     PThemeType.ABORTED_ROUNDED_BINARY,
            Exposition.P_MODULE_MEASURES_DICT:           {
                "P1":   MR(43, 65),
                "P2.1": MR(65, 81),
            },
            Exposition.P_MODULE_PHRASE_DICT:             {
                "P1": PhraseStructure.PERIOD,
            },
            Exposition.P_THEME_OPENING_KEY:              Key.BES_MAJOR,
            Exposition.P_THEME_ENDING_KEY:               Key.BES_MAJOR,
            Exposition.P_THEME_ENDING_CADENCE:           Cadence.IAC_TONIC_BASS_PEDAL,
            Exposition.P_THEME_PAC_MEASURES_LIST:        [MR(65)],

            Exposition.TR_THEME_MEASURES:                MR(81, 103),
            Exposition.TR_THEME_TYPE:                    TRThemeType.DISSOLVING_REPRISE,
            Exposition.TR_MODULE_MEASURES_DICT:          {
                "TR1.1": MR(81, 95),
                "TR1.2": MR(95, 103),
            },
            Exposition.TR_THEME_OPENING_KEY:             Key.BES_MAJOR,
            Exposition.TR_THEME_ENERGY:                  EnergyChange.ENERGY_STASIS_FORTE,
            Exposition.TR_THEME_HAMMER_BLOW_COUNT:       0,
            Exposition.TR_THEME_CHROMATIC_PREDOMINANT:   True,
            Exposition.TR_THEME_ENDING_KEY:              Key.F_MINOR,
            Exposition.TR_THEME_ENDING_CADENCE:          Cadence.HC,

            Exposition.MC_MEASURES:                      MR(103, 106),
            Exposition.MC_STYLE:                         MC.CAESURA_FILL_CASCADE,
            Exposition.MC_FILL_KEY:                      Key.F_MAJOR,

            Exposition.S_THEME_MEASURES:                 MR(107, 177),
            Exposition.S_THEME_TYPE:                     SThemeType.MULTI_MODULAR_S,
            Exposition.S_MODULE_MEASURES_DICT:           {
                "S1.1": MR(107, 112),
                "S1.2": MR(113, 120),
                "S1.3": MR(121, 134),
                "S1.4": MR(135, 141),
                "S2.1": MR(141, 158),
                "S2.2": MR(159, 177)
            },
            Exposition.S_THEME_OPENING_KEY:              Key.F_MAJOR,
            Exposition.S_THEME_OTHER_KEYS_LIST:          [
                Key.D_MINOR,
            ],
            Exposition.S_THEME_ENDING_KEY:               Key.BES_MAJOR,
            Exposition.S_THEME_STRONG_PAC_MEASURES_LIST: [MR(177)],
            Exposition.S_THEME_ATTEN_PAC_MEASURES_LIST:  [MR(141)],
            Exposition.S_THEME_EVADED_PAC_MEASURES_LIST: [MR(163), MR(167)],
            Exposition.S_THEME_ENDING_CADENCE:           Cadence.PAC_MAJOR,

            Exposition.EEC_ESC_SECURED:                  True,
            Exposition.EEC_ESC_MEASURE:                  MR(177),

            Exposition.C_THEME_MEASURES_INCL_C_RT:       MR(177, 187),
            Exposition.C_THEME_TYPE:                     CThemeType.FORTE_P_DERIVATION_C,
            Exposition.C_MODULE_MEASURES_DICT:           {
                'C1': MR(177, 187)
            },
            Exposition.C_THEME_COMMENTS:                 "Could maybe consider m. 141 EEC and S2 as C0 but the m. 141 "
                                                         "cadence is attenuated, and the S2.1 motives after m. 141 "
                                                         "link back to diminution of bass cadential 1.4 motives "
                                                         "in m. 135-140. Also, C-RT is in first ending which has"
                                                         "no measure numbers since not present in second ending.",
            Exposition.C_THEME_OPENING_KEY:              Key.F_MAJOR,
            Exposition.C_THEME_ENDING_KEY_BEFORE_C_RT:   Key.F_MAJOR,
            Exposition.C_RT_PRESENT:                     True,
            Exposition.C_RT_ENDING_KEY:                  Key.BES_MAJOR,
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
            Recapitulation.COMMENTS:                         "If include wind-up as P0, recap could begin in "
                                                             "m. 347 (especially since tonic starts there)",
            Recapitulation.MEASURES:                         MR(337, 461),

            Recapitulation.P_THEME_MEASURES:                 MR(337, 351),
            Recapitulation.P_MODULE_MEASURES_DICT:           {
                "P1": MR(337, 351),
            },
            Recapitulation.P_MODULE_PHRASE_DICT: {
              "P1":  PhraseStructure.ANTECEDENT,
            },
            Recapitulation.P_THEME_CHANGE_FROM_EXPOSITION:   "P1 vastly truncated (no consequent) and "
                                                             "P2 absent entirely",
            Recapitulation.TR_THEME_MEASURES:                MR(351, 377),
            Recapitulation.TR_MODULE_MEASURES_DICT:          {
                "TR1.1": MR(351, 369),
                "TR1.2": MR(369, 377),
            },
            Recapitulation.TR_THEME_ENDING_KEY:              Key.BES_MAJOR,

            Recapitulation.MC_MEASURES:                      MR(377, 380),

            Recapitulation.S_THEME_MEASURES:                 MR(381, 451),
            Recapitulation.S_MODULE_MEASURES_DICT:           {
                "S1.1": MR(381, 386),
                "S1.2": MR(387, 394),
                "S1.3": MR(395, 408),
                "S1.4": MR(409, 415),
                "S2.1": MR(415, 432),
                "S2.2": MR(433, 451)
            },
            Recapitulation.S_THEME_OPENING_KEY:              Key.BES_MAJOR,
            Recapitulation.S_THEME_STRONG_PAC_MEASURES_LIST: [MR(451)],
            Recapitulation.S_THEME_ATTEN_PAC_MEASURES_LIST:  [MR(415)],
            Recapitulation.S_THEME_EVADED_PAC_MEASURES_LIST: [MR(437), MR(441)],
            Recapitulation.S_THEME_ENDING_KEY:               Key.BES_MAJOR,
            Recapitulation.EEC_ESC_MEASURE:                  MR(451),

            Recapitulation.C_THEME_MEASURES_INCL_C_RT:       MR(451, 461),
            Recapitulation.C_MODULE_MEASURES_DICT:           {
                "C1": MR(451, 461),
            },
            Recapitulation.C_THEME_OPENING_KEY:              Key.BES_MAJOR,
            Recapitulation.C_THEME_ENDING_KEY_BEFORE_C_RT:   Key.BES_MAJOR,
            Recapitulation.C_RT_PRESENT:                     False,
        }

        recap_dict.update(recap_updates)
        return recap_dict

    @classmethod
    def coda_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Coda.MEASURES:         MR(461, 498),
            Coda.P_THEME_RECALLED: True,
            Coda.OPENING_KEY:      Key.BES_MAJOR,
            Coda.ENDING_KEY:       Key.BES_MAJOR,
        }
