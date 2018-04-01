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

class Beethoven1(PieceDataClass):
    @classmethod
    def piece_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Piece.ID:            "beethoven1",
            Piece.COMPOSER_ID:   Beethoven.id(),
            Piece.NAME:          "Symphony No. 1",
            Piece.CATALOGUE_ID:  "Op. 21",
            Piece.GLOBAL_KEY:    Key.C_MAJOR,
            Piece.PREMIER_DATE:  date(1800, 4, 2),
            Piece.YEAR_STARTED:  1795,
            Piece.NUM_MOVEMENTS: 4,
            Piece.PIECE_TYPE:    PieceType.SYMPHONY
        }


#################
# Sonata(s)
#################

class Beethoven1_1(SonataDataClass):
    @classmethod
    def sonata_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Sonata.PIECE_ID:                 Beethoven1.id(),
            Sonata.MOVEMENT_NUM:             1,
            Sonata.SONATA_TYPE:              SonataType.TYPE_3,
            Sonata.GLOBAL_KEY:               Key.C_MAJOR,
            Sonata.MEASURE_COUNT:            298,
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
            Introduction.MEASURES:                MeasureRange(1, 12),
            Introduction.OPENING_TEMPO:           "Adagio molto",
            Introduction.OPENING_KEY:             Key.F_MAJOR,
            Introduction.INTRODUCTION_OTHER_KEYS: [Key.G_MAJOR],
            Introduction.ENDING_KEY:              Key.C_MAJOR,
        }

    @classmethod
    def exposition_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Exposition.MEASURES:                         MeasureRange(13, 109),
            Exposition.OPENING_TEMPO:                    "Allegro con brio",

            Exposition.P_THEME_MEASURES:                 MeasureRange(13, 33),
            Exposition.P_THEME_OPENING_KEY:              Key.C_MAJOR,
            Exposition.P_MODULE_PHRASE_STRUCTURE:        [PhraseStructure.COMPOUND_SENTENCE],
            Exposition.P_THEME_ENDING_KEY:               Key.C_MAJOR,
            Exposition.P_THEME_ENDING_CADENCE:           Cadence.PAC_MAJOR,

            Exposition.TR_THEME_MEASURES:                MeasureRange(33, 52),
            Exposition.TR_THEME_OPENING_KEY:             Key.C_MAJOR,
            Exposition.TR_THEME_ENERGY:                  EnergyChange.ENERGY_GAIN_CRESCENDO,
            Exposition.TR_THEME_DOMINANT_LOCK:           True,
            Exposition.TR_THEME_CHROMATIC_PREDOMINANT:   True,
            Exposition.TR_THEME_HAMMER_BLOW_COUNT:       3,
            Exposition.TR_THEME_ENDING_KEY:              Key.C_MAJOR,
            Exposition.TR_THEME_ENDING_CADENCE:          Cadence.HC,

            Exposition.MC_STYLE:                         MedialCaesura.GENERAL_PAUSE,
            Exposition.MC_MEASURES:                      MeasureRange(52),

            Exposition.S_THEME_MEASURES:                 MeasureRange(53, 88),
            Exposition.S_MODULE_MEASURES:                {
                "S1": MeasureRange(53, 77),
                "S2": MeasureRange(77, 88),
            },
            Exposition.S_THEME_OPENING_KEY:              Key.G_MAJOR,
            Exposition.S_ATTENUATED_EVADED_PAC_MEASURES: [MeasureRange(77)],
            Exposition.S_THEME_OTHER_KEYS:               [Key.G_MINOR],
            Exposition.S_THEME_ENDING_KEY:               Key.G_MAJOR,
            Exposition.S_THEME_ENDING_CADENCE:           Cadence.PAC_MAJOR,
            Exposition.EEC_ESC_SECURED:                  True,
            Exposition.EEC_ESC_MEASURE:                  MeasureRange(88),

            Exposition.C_THEME_MEASURES:                 MeasureRange(88, 109),
            Exposition.C_THEME_OPENING_KEY:              Key.G_MAJOR,
            Exposition.C_THEME_P_BASED:                  True,
        }

    @classmethod
    def development_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Development.MEASURES:                   MeasureRange(110, 178),
            Development.OPENING_KEY:                Key.A_MAJOR,
            Development.DEVELOPMENT_OTHER_KEYS:     [
                Key.G_MAJOR,
                Key.C_MINOR,
                Key.F_MINOR,
                Key.BES_MAJOR,
                Key.EES_MAJOR,
                Key.F_MINOR,
                Key.G_MINOR,
                Key.D_MINOR,
            ],
            Development.DEVELOPMENT_ENDING_KEY:     Key.A_MINOR,
            Development.DEVELOPMENT_ENDING_CADENCE: Cadence.HC

        }

    @classmethod
    def recapitulation_attribute_dict(cls) -> Dict[Field, Any]:
        recap_dict = cls.exposition_attribute_dict_without_fields_unlikely_to_be_same()

        recap_updates = {
            Recapitulation.MEASURES:                         MeasureRange(178, 298),

            Recapitulation.P_THEME_MEASURES:                 MeasureRange(178, 198),
            Recapitulation.P_THEME_CHANGE_FROM_EXPOSITION:   "P1.3 extended and P1.4 elided",
            Recapitulation.P_THEME_ENDING_KEY:               Key.G_MAJOR,
            Recapitulation.P_THEME_ENDING_CADENCE:           Cadence.PAC_MAJOR,

            Recapitulation.TR_THEME_MEASURES:                MeasureRange(198, 204),
            Recapitulation.TR_THEME_CHANGE_FROM_EXPOSITION:  "TR Theme shortened and no exposition TR motives appear",
            Recapitulation.TR_THEME_ENDING_KEY:              Key.C_MAJOR,
            Recapitulation.MC_MEASURES:                      MeasureRange(204, 205),
            Recapitulation.MC_STYLE:                         MedialCaesura.CAESURA_FILL,
            Recapitulation.MC_CHANGE_FROM_EXPOSITION:        "",
            Recapitulation.S_THEME_MEASURES:                 MeasureRange(206, 241),
            Recapitulation.S_ATTENUATED_EVADED_PAC_MEASURES: [MeasureRange(230)],
            Recapitulation.S_MODULE_MEASURES:                {
                "S1": MeasureRange(206, 230),
                "S2": MeasureRange(230, 241),
            },
            Recapitulation.S_THEME_OPENING_KEY:              Key.C_MAJOR,
            Recapitulation.S_THEME_OTHER_KEYS:               [Key.C_MINOR],
            Recapitulation.S_THEME_ENDING_KEY:               Key.C_MAJOR,
            Recapitulation.EEC_ESC_MEASURE:                  MeasureRange(241),

            Recapitulation.C_THEME_MEASURES:                 MeasureRange(241, 259),
            Recapitulation.C_THEME_OPENING_KEY:              Key.C_MAJOR,
        }

        recap_dict.update(recap_updates)
        return recap_dict

    @classmethod
    def coda_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Coda.MEASURES:        MeasureRange(259, 298),
            Coda.OPENING_KEY:     Key.F_MAJOR,
            Coda.CODA_OTHER_KEYS: [Key.D_MINOR],
            Coda.ENDING_KEY:      Key.C_MAJOR,
        }
