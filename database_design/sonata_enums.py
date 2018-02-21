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


if __name__ == '__main__':
    pass