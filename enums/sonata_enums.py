#!/usr/bin/env python
"""
A module containing enums for use in picklist-style fields for the sonata archive
"""


class SonataType(object):
    """
    An enum for a sonata type
    """

    TYPE_1 = "Type 1"
    TYPE_2 = "Type 2"
    TYPE_3 = "Type 3"
    TYPE_4 = "Type 4"
    TYPE_5 = "Type 5"


class PieceType(object):
    """
    An enum for a piece type
    """

    # Orchestral Works
    SYMPHONY = "Symphony"
    SYMPHONIC_POEM = "Symphonic Poem"
    OPERA_OVERTURE = "Opera Overture"
    PIANO_CONCERTO = "Piano Concerto"
    VIOLIN_CONCERTO = "Violin Concerto"

    # Solo Piano Works
    PIANO_SONATINA = "Piano Sonatina"
    PIANO_SONATA = "Piano Sonata"
    PIANO_SONG_WITHOUT_WORDS = "Piano Song Without Words"
    PIANO_SCHERZO = "Piano Scherzo"
    PIANO_BALLADE = "Piano Ballade"
    PIANO_WALTZ = "Piano Waltz"
    PIANO_POLONAISE = "Piano Polonaise"
    PIANO_INTERMEZZO = "Piano Intermezzo"
    PIANO_PRELUDE = "Piano Prelude"
    PIANO_NOCTURNE = "Piano Nocturne"
    PIANO_ETUDE = "Piano Étude"
    PIANO_FANTASY = "Piano Fantasy"
    PIANO_RHAPSODY = "Piano Rhapsody"

    # String Works
    VIOLIN_SONATA = "Violin Sonata"
    STRING_QUARTET = "String Quartet"


class Cadence(object):
    """
    An enum for Types of Cadences
    """

    # Authentic Cadences in Major
    PAC_MAJOR = "PAC (Ⅴ - Ⅰ)"  # PAC means root position with both chords AND soprano on scale degree 1^
    IAC_MAJOR = "IAC (Ⅴ - Ⅰ)"  # Same as PAC except soprano not on scale degree 1^
    IAC_V6_I = "IAC Inverted (V⁶ - Ⅰ)"
    IAC_V_I6 = "IAC Inverted (Ⅴ - Ⅰ⁶)"
    IAC_V6_I6 = "IAC Inverted (Ⅴ⁶ - Ⅰ⁶)"
    IAC_V42_I6 = "IAC Evaded (Ⅴ⁴₂ - Ⅰ⁶)"

    # Authentic Cadences in Minor
    PAC_MINOR = "PAC (Ⅴ - ⅰ)"  # PAC means root position with both chords AND soprano on scale degree 1^
    IAC_MINOR = "IAC (Ⅴ - ⅰ)"  # Same as PAC except soprano not on scale degree 1^
    IAC_V6_i = "IAC Inverted (V⁶ - ⅰ)"
    IAC_V_i6 = "IAC Inverted (Ⅴ - ⅰ⁶)"
    IAC_V6_i6 = "IAC Inverted (Ⅴ⁶ - ⅰ⁶)"
    IAC_V42_i6 = "IAC Evaded (Ⅴ⁴₂ - ⅰ⁶)"

    # Half Cadences
    HC = "HC (ends on V)"  # Standard half cadence that ends on root position V
    HC_V6 = "HC Inverted (ends on Ⅴ⁶)"
    HC_IV6_V = "HC Phrygian (ⅳ⁶ - V)"

    # Deceptive Cadences
    DC_IV = "DC (V - Ⅳ)"
    DC_vi = "DC (V - ⅵ)"
    DC_bVI = "DC (V - ♭Ⅵ)"


class CadenceStrength(object):
    """
    An enum for the strength / style of cadences
    """

    # Strong metric placement on resolution on resolution chord
    STRONG = "Strong"

    # Weak metric placement on resolution chord
    WEAK = "Weak"

    # Seems like will be strong on the first chord but the resolution withers away due to texture or dynamics
    ATTENUATED = "Attenuated"


class PhraseStructure(object):
    """
    An enum for Phrase Structure, using terms from Caplin's Classical Form
    """
    # @formatter:off

    # Tiny (~2-3 measure) Phrase Units
    BASIC_IDEA = "Basic Idea (BI)"               # BI = motivic cell cellhas no cadence
    CONTRASTING_IDEA = "Contrasting Idea (CI)"   # CI = counterpart to BI Half Cadence, or IAC, CI' =

    # Small (~4-5 measure) Phrase Units
    ANTECEDENT = "Antecedent"                           # BI + CI  (ends in HC or IAC)
    CONSEQUENT = "Consequent"                           # BI + CI' (ends in PC or IAC)
    COMPOUND_BASIC_IDEA = "Compound Basic Idea"         # BI + BI  (no cadence)
    PRESENTATION = "Presentation"                       # BI + BI' (no cadence)
    CONTINUATION = "Continuation"                       # Fragmentation / Liquidation of BI  (no cadence)
    CADENTIAL = "Cadential"                             # Cadential Progression  (PAC, HC or IAC)
    CONTINUATION_CADENTIAL = "Continuation + Cadential"

    # Medium (~8-10 measure) Phrase Units
    PERIOD = "Period"           # Antecedent          -> Consequent
    SENTENCE = "Sentence"       # Presentation        -> Continuation + Cadential
    HYBRID_1 = "Hybrid 1"       # Antecedent          -> Continutation
    HYBRID_2 = "Hybrid 2"       # Antecedent          -> Cadential
    HYBRID_3 = "Hybrid 3"       # Compound Basic Idea -> Continuation
    HYBRID_4 = "Hybrid 4"       # Compound Basic Idea -> Consequent

    GRAND_ANTECEDENT = "Grand Antecedent"  # The antecedent of a compound period
    GRAND_CONSEQUENT = "Grand Consequent"  # The consequent of a compound period
    GRAND_DISSOLVING_CONSEQUENT = "Grand Dissolving Consequent"  # A compound period's consequent that liquidates

    # Large (16+ measure) Phrase Units
    COMPOUND_PERIOD = "Compound Period"  # A large period where each ant + cons is a medium phrase structure
    COMPOUND_SENTENCE = "Compound Sentence"  # A large sentence where the presentation contains 2 compound BIs
    COMPOUND_PERIOD_OF_PERIODS = "Compound Period (of Periods)"  # Compound Period where each halves are periods


class EnergyChange(object):
    """
    An enum to describe energy gain / loss / stasis
    """

    ENERGY_GAIN_CRESCENDO = "Energy Gain Crescendo"
    ENERGY_LOSS_DIMINUENDO = "Energy Gain Crescendo"
    ENERGY_STASIS_FORTE = "Energy Stasis Forte"
    ENERGY_STASIS_PIANO = "Energy Stasis Piano"


class MedialCaesura(object):
    """
    An enum to describe MCs
    """

    GENERAL_PAUSE = "General Pause"
    CAESURA_FILL = "Caesura Fill"
    CAESURA_FILL_RISE = "Caesura Fill Rise"
    CAESURA_FILL_CASCADE = "Caesura Fill Cascade"


def measure_number_range(start_measure_num: int, end_measure_num: int):
    """
    Takes start and end measure numbers and turns them into a range

    :param start_measure_num: the start measure (inclusive)
    :param end_measure_num: the end measure (inclusive)
    :return: a range string with both start and end measures
    """
    if start_measure_num > end_measure_num:
        raise Exception("Start measure {} was greater than end measure {}".format(start_measure_num, end_measure_num))
    if start_measure_num == end_measure_num:
        return "m. {}".format(start_measure_num)
    return "mm. {} - {}".format(start_measure_num, end_measure_num)


if __name__ == '__main__':
    pass