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

class Beethoven7(PieceDataClass):
    @classmethod
    def piece_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Piece.ID:             "beethoven7",
            Piece.COMPOSER_ID:    Beethoven.id(),
            Piece.NAME:           "Symphony No. 7",
            Piece.CATALOGUE_ID:   "Op. 92",
            Piece.GLOBAL_KEY:     Key.A_MAJOR,
            Piece.PREMIER_DATE:   date(1813, 12, 8),
            Piece.YEAR_STARTED:   1811,
            Piece.YEAR_COMPLETED: 1812,
            Piece.NUM_MOVEMENTS:  4,
            Piece.PIECE_TYPE:     PieceType.SYMPHONY
        }


#################
# Sonata(s)
#################

class Beethoven7_1(SonataDataClass):
    @classmethod
    def sonata_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Sonata.PIECE_ID:                 Beethoven7.id(),
            Sonata.MOVEMENT_NUM:             1,
            Sonata.SONATA_TYPE:              SonataType.TYPE_3,
            Sonata.GLOBAL_KEY:               Key.A_MAJOR,
            Sonata.MEASURE_COUNT:            450,
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
            Intro.MEASURES:                  MR(1, 62),
            Intro.OPENING_TEMPO:             "Poco sostenuto",
            Intro.OPENING_KEY:               Key.A_MAJOR,
            Intro.OTHER_KEYS_LIST:           [
                Key.C_MAJOR,
                Key.F_MAJOR,
            ],
            Intro.ENDING_KEY:                Key.A_MAJOR,
            Intro.EXPOSITION_WINDUP:         True,
            Intro.EXPOSITION_WINDUP_MEASURE: MR(59),
        }

    @classmethod
    def exposition_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Expo.MEASURES:                   MR(63, 176),
            Expo.OPENING_TEMPO:              "Vivace",
            Expo.CONTINUOUS:                 True,
            Expo.CONTINUOUS_SUBTYPE:         ContinuousSubtype.SUBTYPE_2_EARLY_PAC_REPETITIONS,

            Expo.P_MEASURES:                 MR(63, 88),
            Expo.P_TYPE:                     PThemeType.GRAND_ANTECEDENT,
            Expo.P_MODULE_MEASURES_DICT:     {
                "P1.0": MR(63, 66),
                "P1.1": MR(67, 74),
                "P2.1": MR(75, 80),
                "P2.2": MR(81, 88),
            },
            Expo.P_MODULE_PHRASE_DICT:       {
                "P1.1": PhraseStructure.PERIOD,
                "P2.1": PhraseStructure.PRESENTATION,
                "P2.2": PhraseStructure.SENTENCE,
            },
            Expo.P_MODULE_TYPES_DICT:        {
                "P1.0": PThemeType.RHYTHMIC_STREAM,
            },
            Expo.P_PAC_MEASURES_LIST:        [MR(74)],
            Expo.P_OPENING_KEY:              Key.A_MAJOR,
            Expo.P_ENDING_KEY:               Key.A_MAJOR,
            Expo.P_ENDING_CADENCE:           Cadence.HC,

            Expo.TR_MEASURES:                MR(89, 164),
            Expo.TR_TYPE:                    TRThemeType.MULTI_MODULAR_MIXED_TR,
            Expo.TR_MODULE_MEASURES_DICT:    {
                "TR1.1": MR(89, 96),
                "TR2.1": MR(97, 100),
                "TR2.2": MR(101, 108),
                "TR2.3": MR(109, 112),
                "TR2.4": MR(112, 119),
                "TR2.5": MR(120, 124),
                "TR2.6": MR(124, 130),
                "TR3.1": MR(130, 134),
                "TR4.1": MR(134, 141),
                "TR4.2": MR(142, 152),
                "TR4.3": MR(152, 164),
            },
            Expo.TR_MODULE_PHRASE_DICT:      {
                "TR1.1": PhraseStructure.PERIOD,

            },
            Expo.TR_MODULE_TYPES_DICT:       {
                "TR1.1|TR2.1|TR2.2": TRThemeType.DISSOLVING_RESTATEMENT,
                "TR2.3":             TRThemeType.SUDDEN_INDEPENDENT_INTERRUPTION,
                "TR2.4":             TRThemeType.INDEPENDENT_DEVELOPMENTAL,
                "TR2.5":             TRThemeType.INDEPENDENT_DEVELOPMENTAL,
                "TR2.6":             TRThemeType.CADENTIAL,
                "TR3.1":             TRThemeType.CADENTIAL,
                "TR4.1":             TRThemeType.INDEPENDENT_DEVELOPMENTAL,
                "TR4.2":             TRThemeType.DEVELOPMENTAL_BUILDUP,
                "TR4.3":             TRThemeType.DISSOLVING_RESTATEMENT

            },
            Expo.TR_PAC_MEASURES_LIST:       [MR(96), MR(130), MR(134)],
            Expo.TR_OPENING_KEY:             Key.A_MAJOR,
            Expo.TR_OTHER_KEYS_LIST:         [
                Key.CIS_MINOR,
                Key.AES_MINOR,
            ],
            Expo.TR_MC_EFFECT_MEASURES_LIST: [MR(109)],
            Expo.TR_ENERGY:                  EnergyChange.ENERGY_STASIS_FORTE,
            Expo.TR_HAMMER_COUNT:            0,
            Expo.TR_DOMINANT_LOCK:           False,
            Expo.TR_CHROM_PREDOM:            False,
            Expo.TR_ENDING_KEY:              Key.E_MAJOR,
            Expo.TR_COMMENTS:                """            
"MC-Effect at m. 109 and early" PAC (the candidate E Major EEC) in m. 130, unusually short cadential repetition from m. 130-134 and then 
deformationally expanded repetition until "real" EEC at m. 164.
            """,
            # Since No S, this Ending cadence is thus
            Expo.TR_ENDING_CADENCE:          Cadence.IAC_MAJOR,

            # Continuous, so no MC or S Theme
            Expo.MC_PRESENT:                 False,
            Expo.S_PRESENT:                  False,
            Expo.S_COMMENTS:                 """
There is something somewhat S-like about TR2.4 with the sudden drop to piano and one could maybe consider
TR2.3 MC Effect to actually be a I:HC MC with deformational fill that modulates us to V/iii for the onset of S.
One could perhaps thus argue that TR2.4 is a P-based S (which many casual analysis seems to state),
but one would then have a difficult time deferring the EEC to m. 164 (clear onset of forte P-based C1)
since the cadential repetitions in m. 130 and m. 134 are unusual for S space.

I thus agree with Hepokoski in classifying this as continuous exposition subtype 2, but I do think Beethoven
did intend the TR2.4 to be somewhat in dialogue with S before continuous logic takes over.
            """,

            Expo.EEC_ESC_SECURED:            True,
            Expo.EEC_ESC_MEASURE:            MR(164),
            Expo.EEC_ESC_COMMENTS:           """
EEC secured by a very accented IAC with 5^ in soprano that is elided with the start of P1.1-based C (that begins on 5^).
This elision seems like it obscures what otherwise could have been a PAC, so the IAC is deemed strong enough to secure
the EEC
            """,
            Expo.C_MEASURES_INCL_C_RT:       MR(164, 176),
            Expo.C_TYPE:                     CThemeType.FORTE_P_BASED_C,
            Expo.C_RT_PRESENT:               True,
            Expo.C_MODULE_MEASURES_DICT:     {
                "C1.1": MR(164, 171),
                "C1.2": MR(171, 176)
            },
            Expo.C_MODULE_TYPES_DICT:        {
                "C1.1": CThemeType.FORTE_P_BASED_C,
                "C1.2": CThemeType.FORTE_P_DERIVATION_C,
            },
            Expo.C_OPENING_KEY:              Key.E_MAJOR,
            Expo.C_ENDING_KEY_BEFORE_C_RT:   Key.E_MAJOR,
        }

    @classmethod
    def development_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Development.MEASURES:        MR(177, 274),
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
            Recap.MEASURES:                 MR(274, 388),

            Recap.P_MEASURES:               MR(279, 311),
            Recap.P_MODULE_MEASURES_DICT:   {
                "P1.0": MR(279, 288),
                "P1.1": MR(289, 292),
                "P1.2": MR(293, 300),
                "P1.3": MR(300, 311)
            },
            Recap.P_COMMENTS:               "P1.0 has new violin I countermelody and the half-cadence"
                                            "fermata is expanded into a multi-measure figuration; "
                                            "P1.1 contains a novel tripleted ostinato countermelody "
                                            "throughout",

            Recap.TR_MEASURES:              MR(312, 328),
            Recap.TR_MODULE_MEASURES_DICT:  {
                "TR1.2": MR(312, 328)
            },
            Recap.TR_ENDING_KEY:            Key.F_MAJOR,
            Recap.TR_COMMENTS:              "TR1.1 elided completely in favor of more boisterous TR1.2",

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
        }

        recap_dict.update(recap_updates)
        return recap_dict

    @classmethod
    def coda_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Coda.MEASURES:    MR(389, 450),
            Coda.P_RECALLED:  True,
            Coda.OPENING_KEY: Key.BES_MAJOR,
            Coda.ENDING_KEY:  Key.A_MAJOR,
        }
