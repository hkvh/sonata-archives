#!/usr/bin/env python
"""
A module containing enums for use in picklist-style fields for the sonata archive
"""
from enums.key_enums import RelativeKey


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


class Dynamics(object):
    """
    An enum to describe Dynamics
    """

    PIANISSISSIMO = "Pianississimo (ppp)"
    PIANISSIMO = "Pianissimo (pp)"
    PIANO = "Piano (p)"
    MEZZO_PIANO = "Mezzo-Piano (mp)"
    MEZZO_FORTE = "Mezzo-Forte (mf)"
    FORTE = "Forte (f)"
    FORTISSIMO = "Fortissimo (ff)"
    FORTISSISSIMO = "Fortississimo (fff)"


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
    IAC_TONIC_BASS_PEDAL = "IAC Bass Pedal (Ⅴ over Tonic Pedal)"

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

    # Medium (~8-10 measure) Complete Phrases
    PERIOD = "Period"              # Antecedent          -> Consequent
    SENTENCE = "Sentence"          # Presentation        -> Continuation + Cadential
    HYBRID_1 = "Hybrid 1"          # Antecedent          -> Continutation
    HYBRID_2 = "Hybrid 2"          # Antecedent          -> Cadential
    HYBRID_3 = "Hybrid 3"          # Compound Basic Idea -> Continuation
    HYBRID_4 = "Hybrid 4"          # Compound Basic Idea -> Consequent
    MOZARTIAN_LOOP_SENTENCE = \
        "Mozartian Loop Sentence"  # Presentation of Repeated Cadential Loops -> Continuation + Cadential

    # Large (~16-32 measure) Complete Phrases
    COMPOUND_PERIOD = "Compound Period"  # A large period where each ant + cons is a medium phrase structure
    COMPOUND_SENTENCE = "Compound Sentence"  # A large sentence where the presentation contains 2 compound BIs
    COMPOUND_PERIOD_OF_PERIODS = "Compound Period (of Periods)"  # Compound Period where both halves are periods

    # Larger (Often 32+ measure) Miniature Forms that can serve as Phrase Structures
    TERNARY = "Ternary"  # ABA Form with contrasting middle (i.e. Minuet and Trio, Scherzo and Trio)
    BINARY = "Binary"    # AB Form
    ROUNDED_BINARY = "Rounded Binary"  # ABA' form (like ternary but A' reprise shorter than A)
    LYRIC_BINARY = "Lyric Binary"  # Special case of Rounded Binary: aa'ba'

    # @formatter:on


class PThemeType(object):
    """
    An enum to describe P Theme Type. Besides the P => TR merger, all of them should end with a phrase (i.e. some
    cadence.)
    """
    # Grows from generative fragments to a Teleogical goal
    GENERATIVE_TO_TELEOLOGICAL = "Generative to Teleological P"

    # The catch-all to describe a P that completes its phrase and is not an antecedent / has nothing elided by TR
    # For this, the specific phrase type should be handled by the P Phrase Types
    SELF_CONTAINED_PHRASE = "P as Self-Contained Phrase(s)"

    # Partial P => TR merger where P's completed phrase left in a state for TR to finish it
    # (I call this a partial merger because it means P+TR together form some type of phrase structure themselves)
    ANTECEDENT = "P as Antecedent Phrase"
    GRAND_ANTECEDENT = "P as Grand Antecedent"
    GRAND_ANTECEDENT_PERIOD = "P as Grand Antecedent (Itself a Period)"
    GRAND_ANTECEDENT_SENTENCE = "P as Grand Antecedent (Itself a Sentence)"
    GRAND_ANTECEDENT_HYBRID_1 = "P as Grand Antecedent (Itself a Hybrid 1)"
    GRAND_ANTECEDENT_HYBRID_2 = "P as Grand Antecedent (Itself a Hybrid 2)"
    GRAND_ANTECEDENT_HYBRID_3 = "P as Grand Antecedent (Itself a Hybrid 3)"
    GRAND_ANTECEDENT_HYBRID_4 = "P as Grand Antecedent (Itself a Hybrid 4)"
    ABORTED_ROUNDED_BINARY = "P as Aborted Rounded Binary (No Reprise)"  # An ABA' binary where the A' will become TR

    # Full P => TR merger where P + TR are so fully elided that they serve as a single phrase.
    # (The Only P that doesn't end in any cadence)
    P_TR_MERGER_SENTENCE_PRESENTATION = "P=>TR Merger: Sentence Presentation"


class ContinuousSubtype(object):
    """
    An enum to describe subtypes of continuous expositions/recapitulations (i.e. sonata blocks missing MC and S)
    """
    SUBTYPE_1_EXPANSION_SECTION = "Subtype 1: Expansion Section"
    SUBTYPE_2_EARLY_PAC_REPETITIONS = "Subtype 2: Early PAC with Reiterations of Cadence"


class TRThemeType(object):
    """
    An enum to describe TR Types. Besides the P=>TR Merger, all begin with the start of a phrase (i.e after a cedence)
    """

    # The catch-all categories for an independent TR that is not directly emulating P at the outset
    INDEPENDENT_SEPARATELY_THEMATIZED = "Independent Separately Thematized TR"
    INDEPENDENT_DEVELOPMENTAL = "Independent Developmental TR"

    # TR starts like P but is not taking over the completion of the P module left ambiguous
    DISSOLVING_RESTATEMENT = "Dissolving Restatement TR"  # Starts as an initial restatement to any completed P
    DISSOLVING_CONSEQUENT_RESTATEMENT = "Dissolving Consequent Restatement TR"  # Starts like P's completed consequent
    DISSOLVING_CONTINUATION_RESTATEMENT = "Dissolving Consequent Restatement TR"  # Starts like P's completed continuation

    # Partial P => TR merger where TR reacts and beings as a quasi-P module given how P left the phrase
    # (I call this a partial merger because it means P+TR together form some type of phrase structure themselves)
    DISSOLVING_CONSEQUENT = "Dissolving Consequent TR"  # Starts as Consequent to P Antecedent (P+TR = Grand Period)
    DISSOLVING_CONTINUATION = "Dissolving Continuation TR"  # Starts as Continuation to P Antecedent (P+TR = Grand Hybrid1)
    DISSOLVING_REPRISE = "Dissolving Reprise TR"  # Elides the A' in ABA' form (P+TR = Rounded Binary)

    # Full P => TR merger where P + TR are so fully elided that they serve as a single phrase.
    # (The Only TR that doesn't start with the beginning of a phrase)
    P_TR_MERGER_SENTENCE_CONTINUATION = "P=>TR Merger: Sentence Continuation"

    # This is an unusual full P => TR merger because the consequent does not dissolve in usual TR rhetoric
    # (Associated with normal Antecedent P)
    P_TR_MERGER_MODULATING_CONSEQUENT = "P=>TR Merger: Period Modulating Consequent"

    # For transitions that are more than one category, this should be used as TR Type and the different modules of TR
    # should be given the classifications above in TR_Theme_Module_Types (usually left blank)
    MULTI_MODULAR_MIXED_TR = "Multimodular (Mixed) TR"

    # For Dissolving Types, sometimes there is a middle module that is suddenly different
    SUDDEN_INDEPENDENT_INTERRUPTION = "Sudden Independent Interruption TR"


class EnergyChange(object):
    """
    An enum to describe energy gain / loss / stasis
    """

    ENERGY_GAIN_CRESCENDO = "Energy Gain Crescendo"
    ENERGY_LOSS_DIMINUENDO = "Energy Loss Diminuendo"
    ENERGY_STASIS_FORTE = "Energy Stasis Forte"
    ENERGY_STASIS_PIANO = "Energy Stasis Piano"


class MC(object):
    """
    An enum to describe MC Styles with a static method to compute MC Types from a Relative Key and Cadence Type
    """

    GENERAL_PAUSE = "General Pause"
    GENERAL_PAUSE_WITH_S0 = "General Pause with S0"
    CAESURA_FILL = "Caesura Fill"
    DEFORMATION_CAESURA_FILL = "Deformational Caesura Fill"
    CAESURA_FILL_RISE = "Caesura Fill Rise"
    CAESURA_FILL_CASCADE = "Caesura Fill Cascade"
    CAESURA_FILL_CASCADE_AS_S0 = "Caesura Fill Cascade as S0"

    @staticmethod
    def compute_mc_type(relative_key: str, cadence_type: str):
        """
        Given a relative key
        :param relative_key: a relative key enum level string like V
        :param cadence_type: a cadence type enum level string PAC (V - I)
        :return: the appropriate MC Type, like V: PAC (splitting cadence on ( and taking the first part)
        """
        return "{}: {} MC".format(relative_key, cadence_type.split('(')[0].rstrip())


class SThemeType(object):
    """
    An enum to describe S Theme Types.
    """

    # For S Themes with Multiple Modules
    MULTI_MODULAR_S = "Multimodular S (MMS)"
    TRI_MODULAR_S = "Trimodular S (TMS)"  # Special case of MMS

    # General S Types that can be the full S module
    BUSTLING_GALANT = "Bustling Galant S"
    P_BASED_S = "P-Based S"
    LYRICAL_CANTABILE = "Lyrical Cantabile S"
    CONTRASTING_P_DERIVATION = "Contrasting P-Derivation S"
    LEARNED_STYLE_FUGAL_IMITATIVE = "\"Learned-Style\" S"
    VIRTUOSIC_FIGURATION = "Virtuosic Figuration S"

    # S Types for specific S modules (unlikely to apply to all of S)
    OMINOUS_THREATENING = "Ominous Threatening S"
    HEROIC_CADENTIAL = "Heroic Cadential S"
    MISCHEIVOUS_LAMENT = "Mischeivous Lament S"
    DISASTROUS_FAILED_CADENTIAL = "Disastrous Failed Cadential S"
    RECOVERED_CADENTIAL = "Restoration to Cadential S"
    FORTE_PIANO_ALTERNATING = "Forte / Piano Alternating S"


class CThemeType(object):
    """
    An enum to describe C Theme Types.
    """

    # For C Types with Multiple Modules
    MULTI_MODULAR_C = "Multimodular C"

    FORTE_P_BASED_C = "Forte P-Based C"  # For those that very closely match P
    PIANO_P_BASED_C = "Piano P-Based C"

    S_C_PRE_EEC = "S^C (pre-EEC)"

    FORTE_P_DERIVATION_C = "Forte P-Derivation C"  # For those that are loosely derived from motives in P
    PIANO_P_DERIVATION_C = "Piano P-Derivation C"

    FORTE_TR_BASED_C = "Forte TR-Based C"
    PIANO_TR_BASED_C = "Piano TR-Based C"

    NEW_THEME_C = "New Theme C"
    CODETTA_CADENTIAL = "Codetta Cadential C"
    C_AS_S_AFTERMATH = "C as S Aftermath"
    CRESCENDO_ONSET = "Crescendo Onset C"
    PIANO_AFTERTHOUGHT = "Piano Afterthought C"


if __name__ == '__main__':
    print(MC.compute_mc_type(RelativeKey.MAJOR_DOMINANT, Cadence.IAC_V6_I))
