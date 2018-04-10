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

class Beethoven3(PieceDataClass):
    @classmethod
    def piece_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Piece.ID:             "beethoven3",
            Piece.COMPOSER_ID:    Beethoven.id(),
            Piece.NAME:           "Symphony No. 3",
            Piece.CATALOGUE_ID:   "Op. 55",
            Piece.NICKNAME:       "Eroica",
            Piece.GLOBAL_KEY:     Key.EES_MAJOR,
            Piece.PREMIER_DATE:   date(1805, 4, 7),
            Piece.YEAR_STARTED:   1802,
            Piece.YEAR_COMPLETED: 1804,
            Piece.NUM_MOVEMENTS:  4,
            Piece.PIECE_TYPE:     PieceType.SYMPHONY
        }


#################
# Sonata(s)
#################

class Beethoven3_1(SonataDataClass):
    @classmethod
    def sonata_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Sonata.PIECE_ID:                 Beethoven3.id(),
            Sonata.MOVEMENT_NUM:             1,
            Sonata.SONATA_TYPE:              SonataType.TYPE_3,
            Sonata.GLOBAL_KEY:               Key.EES_MAJOR,
            Sonata.MEASURE_COUNT:            701,
            Sonata.INTRODUCTION_PRESENT:     True,
            Sonata.DEVELOPMENT_PRESENT:      True,
            Sonata.CODA_PRESENT:             True,
            Sonata.EXPOSITION_REPEAT:        True,
            Sonata.DEVELOPMENT_RECAP_REPEAT: False,

            # Delete this attribute if did not render a lilypond image for this sonata
            Sonata.LILYPOND_IMAGE_SETTINGS:  {Sonata.IMAGE_WIDTH: 560}
        }

    @classmethod
    def introduction_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Introduction.MEASURES:      MR(1, 2),
            Introduction.OPENING_TEMPO: "Adagio molto",
            Introduction.OPENING_KEY:   Key.EES_MAJOR,
            Introduction.ENDING_KEY:    Key.EES_MAJOR,
        }

    @classmethod
    def exposition_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Exposition.MEASURES:                       MR(3, 153),
            Exposition.OPENING_TEMPO:                  "Allegro con brio",

            Exposition.P_THEME_MEASURES:               MR(3, 37),
            Exposition.P_THEME_TYPE:                   PThemeType.COMPLETED_PHRASE_NON_ANTECEDENT,
            Exposition.P_MODULE_MEASURES_DICT:         {
                "P1": MR(3, 15),
                "P2": MR(15, 37),
            },
            Exposition.P_THEME_OPENING_KEY:            Key.EES_MAJOR,
            Exposition.P_THEME_ENDING_KEY:             Key.EES_MAJOR,
            Exposition.P_THEME_ENDING_CADENCE:         Cadence.PAC_MAJOR,
            Exposition.P_THEME_PAC_MEASURES_LIST:      [MR(15), MR(37)],

            Exposition.TR_THEME_MEASURES:              MR(37, 45),
            Exposition.TR_THEME_TYPE:                  TRThemeType.DISSOLVING_RESTATEMENT,
            Exposition.TR_THEME_OPENING_KEY:           Key.EES_MAJOR,
            Exposition.TR_THEME_ENERGY:                EnergyChange.ENERGY_STASIS_FORTE,
            Exposition.TR_THEME_HAMMER_BLOW_COUNT:     0,
            Exposition.TR_THEME_CHROMATIC_PREDOMINANT: True,
            Exposition.TR_THEME_ENDING_KEY:            Key.BES_MAJOR,
            Exposition.TR_THEME_ENDING_CADENCE:        Cadence.HC,

            Exposition.MC_STYLE:                       MC.CAESURA_FILL_CASCADE_AS_S0,
            Exposition.MC_MEASURES:                    MR(45, 56),

            Exposition.S_THEME_MEASURES:               MR(45, 83),
            Exposition.S_MODULE_MEASURES_DICT:         {
                "S0": MR(45, 56),
                "S1": MR(57, 83),
            },
            Exposition.S_THEME_OPENING_KEY:            Key.BES_MAJOR,
            Exposition.S_THEME_ENDING_KEY:             Key.BES_MAJOR,
            Exposition.S_THEME_ENDING_CADENCE:         Cadence.PAC_MAJOR,
            Exposition.EEC_ESC_SECURED:                True,
            Exposition.EEC_ESC_MEASURE:                MR(83),
            Exposition.C_THEME_MEASURES_INCL_C_RT:     MR(83, 153),
            Exposition.C_MODULE_MEASURES_DICT:         {
                "C0": MR(83, 109),
                "C1": MR(109, 153),
            },
            Exposition.C_THEME_OPENING_KEY:            Key.BES_MAJOR,
            Exposition.C_THEME_ENDING_KEY_BEFORE_C_RT: Key.BES_MAJOR
        }

    @classmethod
    def development_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Development.MEASURES:               MR(154, 398),
            Development.OPENING_KEY:            Key.C_MAJOR,
            Development.OTHER_KEYS_LIST:        [
                Key.C_MINOR,
                Key.CIS_MINOR,
                Key.D_MINOR,
                Key.G_MINOR,
                Key.AES_MAJOR,
                Key.F_MINOR,
                Key.G_MINOR,
                Key.A_MINOR,
                Key.E_MINOR,
                Key.C_MAJOR,
                Key.C_MINOR,
                Key.EES_MAJOR,
                Key.EES_MINOR,
                Key.GES_MAJOR,
                Key.EES_MINOR,
                Key.CES_MAJOR,
                Key.EES_MINOR,
            ],
            Development.DEVELOPMENT_THEME_PRESENT: True,
            Development.DEVELOPMENT_THEME_KEYS: [
                Key.E_MINOR,
                Key.EES_MINOR,
            ],
            Development.ENDING_KEY:             Key.EES_MAJOR,
            Development.ENDING_CADENCE:         Cadence.PAC_MAJOR

        }

    @classmethod
    def recapitulation_attribute_dict(cls) -> Dict[Field, Any]:
        recap_dict = cls.exposition_attribute_dict_without_fields_unlikely_to_be_same()

        recap_updates = {
            Recapitulation.MEASURES:                        MR(398, 556),

            Recapitulation.P_THEME_MEASURES:                MR(398, 408),
            Recapitulation.P_MODULE_MEASURES_DICT:          {
                "P1": MR(398, 408),
                "P2": MR(408, 430),
            },
            Recapitulation.P_THEME_OTHER_KEYS_LIST:         [
                Key.F_MAJOR,
            ],

            Recapitulation.TR_THEME_MEASURES:               MR(430, 448),

            Recapitulation.TR_THEME_ENDING_KEY:             Key.EES_MAJOR,
            Recapitulation.TR_THEME_CHANGE_FROM_EXPOSITION: "Middle section lengthened",

            Recapitulation.MC_MEASURES:                    MR(448, 459),

            Recapitulation.S_THEME_MEASURES:               MR(448, 486),
            Recapitulation.S_MODULE_MEASURES_DICT:         {
                "S0": MR(448, 459),
                "S1": MR(460, 486),
            },
            Recapitulation.S_THEME_OPENING_KEY:            Key.EES_MAJOR,
            Recapitulation.S_THEME_ENDING_KEY:             Key.EES_MAJOR,
            Recapitulation.EEC_ESC_MEASURE:                MR(486),

            Recapitulation.C_THEME_MEASURES_INCL_C_RT:     MR(486, 556),
            Recapitulation.C_MODULE_MEASURES_DICT:         {
                "C0": MR(486, 512),
                "C1": MR(512, 556),
            },
            Recapitulation.C_THEME_OPENING_KEY:            Key.EES_MAJOR,
            Recapitulation.C_THEME_ENDING_KEY_BEFORE_C_RT: Key.EES_MAJOR
        }

        recap_dict.update(recap_updates)
        return recap_dict

    @classmethod
    def coda_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Coda.MEASURES:                   MR(557, 701),
            Coda.P_THEME_RECALLED:           True,
            Coda.DEVELOPMENT_THEME_RECALLED: True,
            Coda.OPENING_KEY:                Key.DES_MAJOR,
            Coda.OTHER_KEYS_LIST:            [
                Key.C_MAJOR,
                Key.F_MINOR,
                Key.EES_MINOR,
            ],
            Coda.ENDING_KEY:                 Key.EES_MAJOR,
        }
