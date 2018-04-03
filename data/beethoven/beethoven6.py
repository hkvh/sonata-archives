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
            # Sonata.LILYPOND_IMAGE_SETTINGS:  {Sonata.IMAGE_WIDTH: 660}
        }

    @classmethod
    def introduction_attribute_dict(cls) -> Dict[Field, Any]:
        return {

        }

    @classmethod
    def exposition_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Exposition.MEASURES:                       MeasureRange(1, 138),
            Exposition.OPENING_TEMPO:                  "Allegro ma non troppo",

            Exposition.P_THEME_MEASURES:               MeasureRange(1, 37),
            Exposition.P_THEME_TYPE:                   PrimaryThemeType.ABORTED_ROUNDED_BINARY,
            Exposition.P_MODULE_MEASURES:              {
                "P1.0": MeasureRange(1, 4),
                "P1.1": MeasureRange(5, 29),
                "P1.2": MeasureRange(29, 37),
            },
            Exposition.P_MODULE_PHRASE_STRUCTURE:      {
                "P1.0": PhraseStructure.ANTECEDENT,
                "P1.1": PhraseStructure.SENTENCE,
                "P1.2": PhraseStructure.PRESENTATION,
            },
            Exposition.P_THEME_OPENING_KEY:            Key.BES_MAJOR,
            Exposition.P_THEME_ENDING_KEY:             Key.BES_MAJOR,
            Exposition.P_THEME_STRUCTURAL_PAC_COUNT:   0,

            Exposition.TR_THEME_MEASURES:              MeasureRange(37, 53),
            Exposition.TR_THEME_TYPE:                  TransitionType.DISSOLVING_RESTATEMENT,
            Exposition.TR_THEME_OPENING_KEY:           Key.F_MAJOR,
            Exposition.TR_THEME_ENERGY:                EnergyChange.ENERGY_STASIS_FORTE,
            Exposition.TR_THEME_HAMMER_BLOW_COUNT:     0,
            Exposition.TR_THEME_CHROMATIC_PREDOMINANT: False,
            Exposition.TR_THEME_ENDING_KEY:            Key.F_MAJOR,
            Exposition.TR_THEME_ENDING_CADENCE:        Cadence.IAC_MAJOR,

            Exposition.MC_MEASURES:                    MeasureRange(53, 66),
            Exposition.MC_STYLE:                       MedialCaesura.DEFORMATION_CAESURA_FILL,
            Exposition.MC_FILL_KEY:                    Key.F_MAJOR,
            Exposition.MC_COMMENTS:                    "Series of pause + fill gestures surround tripleted motives – "
                                                       "it is a deformational cascade of MC moments but the net effect "
                                                       "is still the MC that is clearly opening up S space",

            Exposition.S_THEME_MEASURES:               MeasureRange(67, 115),
            Exposition.S_MODULE_MEASURES:              {
                "S1.1": MeasureRange(67, 93),
                "S1.2": MeasureRange(93, 115),
            },
            Exposition.S_THEME_OPENING_KEY:            Key.C_MAJOR,
            Exposition.S_ABORTED_PAC_MEASURES:         [100, 107, 111],
            Exposition.S_THEME_ENDING_KEY:             Key.C_MAJOR,
            Exposition.S_THEME_ENDING_CADENCE:         Cadence.PAC_MAJOR,
            Exposition.EEC_ESC_SECURED:                True,
            Exposition.EEC_ESC_MEASURE:                MeasureRange(115),
            Exposition.C_THEME_MEASURES:               MeasureRange(115, 138),
            Exposition.C_MODULE_MEASURES:              {
                "C1":     MeasureRange(115, 135),
                "C-Link": MeasureRange(135, 138)
            },
            Exposition.C_THEME_OPENING_KEY:            Key.C_MAJOR,
            Exposition.C_THEME_ENDING_KEY:             Key.F_MAJOR,
            Exposition.C_THEME_COMMENTS:               "C1 ends in C Major but 4-bar link veers back to F Major",
        }

    @classmethod
    def development_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Development.MEASURES:               MeasureRange(139, 278),
            Development.OPENING_KEY:            Key.F_MAJOR,
            Development.DEVELOPMENT_OTHER_KEYS: [
                Key.BES_MAJOR,
                Key.D_MAJOR,  # This is a long-enough V of G that it feels like its own key
                Key.G_MAJOR,
                Key.E_MAJOR,  # This is a long-enough V of A that it feels like its own key
                Key.A_MAJOR,
                Key.G_MINOR,
                Key.C_MAJOR,
                Key.F_MAJOR,  # Ends on clear subdominant (almost like an a half cadence ending on IV)
            ],
            Development.DEVELOPMENT_ENDING_KEY: Key.BES_MAJOR,
        }

    @classmethod
    def recapitulation_attribute_dict(cls) -> Dict[Field, Any]:
        recap_dict = cls.exposition_attribute_dict_without_fields_unlikely_to_be_same()

        recap_updates = {
            Recapitulation.COMMENTS:                         "Plagal Cadence leads to soft, almost hidden "
                                                             "onset of Recapitulation: "
                                                             "developmental counter-melodies over P1.0 and P1.1 "
                                                             "make recap-effect subtle until dramatic TR emergence",
            Recapitulation.MEASURES:                         MeasureRange(279, 417),

            Recapitulation.P_THEME_MEASURES:                 MeasureRange(337, 351),
            Recapitulation.P_MODULE_MEASURES:                {
                "P1.0": MeasureRange(279, 288),
                "P1.1": MeasureRange(289, 312),
            },
            Recapitulation.P_MODULE_PHRASE_STRUCTURE: {
                "P1.0": PhraseStructure.ANTECEDENT,
                "P1.1": PhraseStructure.SENTENCE,
            },
            Recapitulation.P_THEME_CHANGE_FROM_EXPOSITION:   "P1.0 has new violin I countermelody and the half-cadence"
                                                             "fermata is expanded into a multi-measure figuration; "
                                                             "P1.1 contains a novel tripleted ostinato and P1.2 is "
                                                             "absent entirely",
            Recapitulation.TR_THEME_MEASURES:                MeasureRange(312, 328),

            Recapitulation.TR_THEME_ENDING_KEY:              Key.F_MAJOR,

            Recapitulation.MC_MEASURES:                      MeasureRange(328, 345),
            Recapitulation.MC_CHANGE_FROM_EXPOSITION:        "MC is slightly extended with additional "
                                                             "tripleted gestures + fill",

            Recapitulation.S_THEME_MEASURES:                 MeasureRange(346, 394),
            Recapitulation.S_MODULE_MEASURES:                {
                "S1.1": MeasureRange(346, 372),
                "S1.2": MeasureRange(372, 394),
            },
            Recapitulation.S_THEME_OPENING_KEY:              Key.F_MAJOR,
            Recapitulation.S_ATTENUATED_EVADED_PAC_MEASURES: [MeasureRange(415)],
            Recapitulation.S_ABORTED_PAC_MEASURES:           [379, 386, 390],
            Recapitulation.S_THEME_ENDING_KEY:               Key.F_MAJOR,
            Recapitulation.EEC_ESC_MEASURE:                  MeasureRange(394),

            Recapitulation.C_THEME_MEASURES:                 MeasureRange(394, 417),
            Recapitulation.C_MODULE_MEASURES:                {
                "C1":     MeasureRange(394, 414),
                "C-Link": MeasureRange(414, 417)
            },
            Recapitulation.C_THEME_OPENING_KEY:              Key.F_MAJOR,
            Recapitulation.C_THEME_ENDING_KEY:               Key.BES_MAJOR,
            Recapitulation.C_THEME_CHANGE_FROM_EXPOSITION:   "C theme transposed up a fourth for tonic resolution (as"
                                                             "expected), leading to C Major C1. However,"
                                                             "this creates a problem for the C link gesture"
                                                             "that was already in tonic in exposition, so the exact"
                                                             " transposition accidentally veers us to the subdominant!"
        }

        recap_dict.update(recap_updates)
        return recap_dict

    @classmethod
    def coda_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Coda.MEASURES:         MeasureRange(418, 512),
            Coda.P_THEME_RECALLED: True,
            Coda.OPENING_KEY:      Key.BES_MAJOR,
            Coda.ENDING_KEY:       Key.F_MAJOR,
        }
