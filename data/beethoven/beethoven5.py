#!/usr/bin/env python
from datetime import date
from typing import Dict, Any

from data.composers import Beethoven
from enums.key_enums import Key
from database_design.sonata_data_classes import PieceDataClass, SonataDataClass
from enums.sonata_enums import PieceType, SonataType, Cadence, EnergyChange, PhraseStructure, \
    MedialCaesura
from database_design.sonata_table_specs import Piece, Sonata, Exposition, Recapitulation, Development, Coda
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
            Sonata.INTRODUCTION_PRESENT:     False,
            Sonata.DEVELOPMENT_PRESENT:      True,
            Sonata.CODA_PRESENT:             True,
            Sonata.EXPOSITION_REPEAT:        True,
            Sonata.DEVELOPMENT_RECAP_REPEAT: False,

            # Delete this attribute if did not render a lilypond image for this sonata
            Sonata.LILYPOND_IMAGE_SETTINGS:  {Sonata.IMAGE_WIDTH: 460}
        }

    @classmethod
    def exposition_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Exposition.OPENING_TEMPO:                              "Allegro con brio",
            Exposition.P_THEME_KEY:                                Key.C_MINOR,
            Exposition.P_THEME_PHRASE_STRUCTURE:                   PhraseStructure.SENTENCE,
            Exposition.P_THEME_ENDING_CADENCE:                     Cadence.HC,

            Exposition.TR_THEME_OPENING_KEY:                       Key.C_MINOR,
            Exposition.TR_THEME_CHROMATICALLY_ALTERED_PREDOMINANT: False,
            Exposition.TR_THEME_HAMMER_BLOW_COUNT:                 2,
            Exposition.TR_THEME_ENERGY:                            EnergyChange.ENERGY_GAIN_CRESCENDO,
            Exposition.TR_THEME_DOMINANT_LOCK:                     False,
            Exposition.TR_THEME_ENDING_KEY:                        Key.E_FLAT_MAJOR,
            # Uses A dim7 / C as vii˚7/B-flat
            Exposition.TR_THEME_ENDING_CADENCE:                    Cadence.HC_V6,
            Exposition.MC_VARIANT:                                 MedialCaesura.GENERAL_PAUSE,

            Exposition.S_THEME_KEY:                                Key.E_FLAT_MAJOR,
            Exposition.S_THEME_ENDING_KEY:                         Key.E_FLAT_MAJOR,
            Exposition.S_THEME_ENDING_CADENCE:                     Cadence.PAC_MAJOR,
            Exposition.EEC_ESC_PRESENT:                            True,

            Exposition.C_THEME_KEY:                                Key.E_FLAT_MAJOR,
            Exposition.C_THEME_P_BASED:                            True,
            Exposition.C_THEME_ENDING_KEY:                         Key.E_FLAT_MAJOR,
        }

    @classmethod
    def development_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Development.OPENING_KEY:             Key.F_MINOR,
            Development.KEYS_TONICIZED:          [
                Key.F_MINOR,
                Key.C_MINOR,
                Key.G_MINOR,
                Key.C_MINOR,
                Key.F_MINOR,
                Key.C_MINOR,
            ],
            Development.RETRANSITION_ENDING_KEY: Key.C_MINOR,
        }

    @classmethod
    def recapitulation_attribute_dict(cls) -> Dict[Field, Any]:
        recap_dict = cls.exposition_attribute_dict()

        recap_changes = {
            Recapitulation.P_THEME_CHANGE_FROM_EXPOSITION:  "Oboe has mournful Adagio interlude",
            Recapitulation.TR_THEME_CHANGE_FROM_EXPOSITION: "Reaches same C dim chord, but resolves differently",
            Recapitulation.S_THEME_KEY:                     Key.C_MAJOR,
            Recapitulation.S_THEME_ENDING_KEY:              Key.C_MAJOR,
            Recapitulation.C_THEME_KEY:                     Key.C_MAJOR,
            Recapitulation.C_THEME_ENDING_KEY:              Key.C_MAJOR,
            Recapitulation.C_THEME_CHANGE_FROM_EXPOSITION:  "Final Cadence elided into onset of Coda"
        }

        recap_dict.update(recap_changes)
        return recap_dict

    @classmethod
    def coda_attribute_dict(cls) -> Dict[Field, Any]:
        return {
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
            Sonata.INTRODUCTION_PRESENT:     False,
            Sonata.DEVELOPMENT_PRESENT:      True,
            Sonata.CODA_PRESENT:             True,
            Sonata.EXPOSITION_REPEAT:        True,
            Sonata.DEVELOPMENT_RECAP_REPEAT: False,

            # Delete this attribute if did not render a lilypond image for this sonata
            Sonata.LILYPOND_IMAGE_SETTINGS:  {Sonata.IMAGE_WIDTH: 620}
        }

    @classmethod
    def exposition_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Exposition.OPENING_TEMPO:                              "Allegro",
            Exposition.P_THEME_KEY:                                Key.C_MAJOR,

            Exposition.TR_THEME_OPENING_KEY:                       Key.C_MAJOR,
            Exposition.TR_THEME_PHRASE_STRUCTURE:                  PhraseStructure.COMPOUND_SENTENCE,
            Exposition.TR_THEME_CHROMATICALLY_ALTERED_PREDOMINANT: False,
            Exposition.TR_THEME_ENERGY:                            EnergyChange.ENERGY_STASIS_FORTE,
            Exposition.TR_THEME_DOMINANT_LOCK:                     True,
            Exposition.TR_THEME_ENDING_KEY:                        Key.G_MAJOR,
            Exposition.TR_THEME_ENDING_CADENCE:                    Cadence.HC,
            Exposition.MC_VARIANT:                                 MedialCaesura.CAESURA_FILL_CASCADE,

            Exposition.S_THEME_PRESENT:                            True,
            Exposition.S_THEME_KEY:                                Key.G_MAJOR,
            Exposition.S_THEME_ENDING_KEY:                         Key.G_MAJOR,
            Exposition.S_THEME_ENDING_CADENCE:                     Cadence.HC,
            Exposition.EEC_ESC_PRESENT:                            False,

            Exposition.C_THEME_PRESENT:                            True,
            Exposition.C_THEME_KEY:                                Key.G_MAJOR,
            Exposition.C_THEME_ENDING_KEY:                         Key.C_MINOR,
        }

    @classmethod
    def development_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Development.OPENING_KEY:             Key.A_MAJOR,
            Development.KEYS_TONICIZED:          [
                Key.A_MAJOR,
                Key.A_MINOR,
                Key.F_MAJOR,
                Key.B_FLAT_MAJOR,
                Key.B_FLAT_MINOR,
                Key.D_FLAT_MAJOR,
                Key.C_MAJOR,
                Key.G_MAJOR,
                Key.C_MINOR,
            ],
            Development.RETRANSITION_ENDING_KEY: Key.C_MINOR,

        }

    @classmethod
    def recapitulation_attribute_dict(cls) -> Dict[Field, Any]:
        recap_dict = cls.exposition_attribute_dict()

        recap_changes = {
            Recapitulation.S_THEME_KEY:        Key.C_MAJOR,
            Recapitulation.S_THEME_ENDING_KEY: Key.C_MAJOR,

            Recapitulation.C_THEME_KEY:        Key.C_MAJOR,
            Recapitulation.C_THEME_ENDING_KEY: Key.C_MAJOR,
        }

        recap_dict.update(recap_changes)
        return recap_dict

    @classmethod
    def coda_attribute_dict(cls) -> Dict[Field, Any]:
        return {
            Coda.OPENING_KEY: Key.C_MAJOR,
            Coda.ENDING_KEY:  Key.C_MAJOR,
        }
