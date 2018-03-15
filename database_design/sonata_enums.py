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


class CadenceType(object):
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

    # Tiny (~2-4 measure) Phrase Units
    BASIC_IDEA = "Basic Idea (BI)"               # BI = motivic cell cellhas no cadence
    CONTRASTING_IDEA = "Contrasting Idea (CI)"   # CI = counterpart to BI Half Cadence, or IAC, CI' =

    # Small (~4-8 measure) Phrase Units
    ANTECEDENT = "Antecedent"                           # BI + CI  (ends in HC or IAC)
    CONSEQUENT = "Consequent"                           # BI + CI' (ends in PC or IAC)
    COMPOUND_BASIC_IDEA = "Compound Basic Idea"         # BI + BI  (no cadence)
    PRESENTATION = "Presentation"                       # BI + BI' (no cadence)
    CONTINUATION = "Continuation"                       # Fragmentation / Liquidation of BI  (no cadence)
    CADENTIAL = "Cadential"                             # Cadential Progression  (PAC, HC or IAC)
    CONTINUATION_CADENTIAL = "Continuation + Cadential"

    # Medium (~8-16 measure) Phrase Units
    PERIOD = "Period"           # Antecedent          -> Consequent
    SENTENCE = "Sentence"       # Presentation        -> Continuation + Cadential
    HYBRID_1 = "Hybrid 1"       # Antecedent          -> Continutation
    HYBRID_2 = "Hybrid 2"       # Antecedent          -> Cadential
    HYBRID_3 = "Hybrid 3"       # Compound Basic Idea -> Continuation
    HYBRID_4 = "Hybrid 4"       # Compound Basic Idea -> Consequent


if __name__ == '__main__':
    pass