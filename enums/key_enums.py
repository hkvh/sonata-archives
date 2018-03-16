#!/usr/bin/env python
"""
A class containing all enums related to pitches, keys and relative keys as well as ways to compute them easily.
"""


class PitchClassException(Exception):
    """
    An exception for when a key is invalid
    """


def validate_pitch_class(pitch_class: int) -> None:
    """
    Confirms that a given pitch class is properly in the range 0 to 11, inclusive

    :param pitch_class: the int to check
    :return: nothing if no problems, else raises a PitchClassException
    """
    if pitch_class < 0 or pitch_class > 11:
        raise PitchClassException("Invalid Key with a pitch class of {}. "
                                  "The pitch class must be between 0 and 11 (inclusive)".format(pitch_class))


class RelativeKey(object):
    """
    An enum for the various relative keys. Uppercase roman numerals mean major, lowerase roman numerals mean minor.
    Since this is only for handling relative major or minor keys, we do not handle diminished or half-diminished or
    seventh chords.

    Note that for consistency, we will use leading flats or sharps relative to the notes in the major scale,
    so the relative major in minor is ♭Ⅲ not Ⅲ. We will also only use flats or sharps after the key if the key is not
    one that commonly occurs in either major or minor and is thus a type of secondary mixture
    """
    MAJOR_TONIC = "Ⅰ"
    MINOR_TONIC = "ⅰ"
    MAJOR_NEAPOLITAN = "♭Ⅱ"
    MINOR_NEAPOLITAN = "♭ⅱ♭"
    MAJOR_SUPERTONIC = "Ⅱ♯"
    MINOR_SUPERTONIC = "ⅱ"
    MAJOR_FLAT_MEDIANT = "♭Ⅲ"
    MINOR_FLAT_MEDIANT = "♭ⅲ♭"
    MAJOR_MEDIANT = "Ⅲ♯"
    MINOR_MEDIANT = "ⅲ"
    MAJOR_SUBDOMINANT = "Ⅳ"
    MINOR_SUBDOMINANT = "ⅳ"
    MAJOR_TRITONE = "♯Ⅳ♯"
    MINOR_TRITONE = "♭Ⅴ♭"
    MAJOR_DOMINANT = "Ⅴ"
    MINOR_DOMINANT = "ⅴ"
    MAJOR_FLAT_SUBMEDIANT = "♭Ⅵ"
    MINOR_FLAT_SUBMEDIANT = "♭ⅵ♭"
    MAJOR_SUBMEDIANT = "Ⅵ♯"
    MINOR_SUBMEDIANT = "ⅵ"
    MAJOR_FLAT_SUBTONIC = "♭Ⅶ"
    MINOR_FLAT_SUBTONIC = "♭ⅶ♭"
    MAJOR_SUBTONIC = "Ⅶ♯"
    MINOR_SUBTONIC = "ⅶ♯"

    MAJOR_RELATIVE_KEY_MAP = {
        0:  MAJOR_TONIC,
        1:  MAJOR_NEAPOLITAN,
        2:  MAJOR_SUPERTONIC,
        3:  MAJOR_FLAT_MEDIANT,
        4:  MAJOR_MEDIANT,
        5:  MAJOR_SUBDOMINANT,
        6:  MAJOR_TRITONE,
        7:  MAJOR_DOMINANT,
        8:  MAJOR_FLAT_SUBMEDIANT,
        9:  MAJOR_SUBMEDIANT,
        10: MAJOR_FLAT_SUBTONIC,
        11: MAJOR_SUBTONIC
    }

    MINOR_RELATIVE_KEY_MAP = {
        0:  MINOR_TONIC,
        1:  MINOR_NEAPOLITAN,
        2:  MINOR_SUPERTONIC,
        3:  MINOR_FLAT_MEDIANT,
        4:  MINOR_MEDIANT,
        5:  MINOR_SUBDOMINANT,
        6:  MINOR_TRITONE,
        7:  MINOR_DOMINANT,
        8:  MINOR_FLAT_SUBMEDIANT,
        9:  MINOR_SUBMEDIANT,
        10: MINOR_FLAT_SUBTONIC,
        11: MINOR_SUBTONIC
    }

    @classmethod
    def get_relative_key(cls, relative_pitch_class: int, minor: bool = False) -> str:
        """
        Given a relative_pitch_class (and whether we want minor or major) returns the implied relative key as a
        prettified roman numeral.

        :param relative_pitch_class: a number from 0 to 11 (inclusive) where 0 = tonic, 7 = dominant etc.
        :param minor: whether we want minor instead of major (defaults to False)
        :return: the string expressing the relative key as a Roman Numeral
        """
        validate_pitch_class(relative_pitch_class)
        if minor:
            return cls.MINOR_RELATIVE_KEY_MAP[relative_pitch_class]
        else:
            return cls.MAJOR_RELATIVE_KEY_MAP[relative_pitch_class]


class KeyStruct(object):
    """
    A class for holding information about a key that will be used to create Key enums
    """
    MAJOR = "Major"
    MINOR = "minor"

    # Church Modes (not used now)
    IONIAN = "Ionian"
    DORIAN = "Dorian"
    PHRYGIAN = "Phryigian"
    LYDIAN = "Lydian"
    MIXOLYDIAN = "Mixolydian"
    AEOLIAN = "Aeolian"
    LOCRIAN = "Locrian"

    def __init__(self, tonic_name: str, tonic_pitch_class: int, minor: bool = False):
        """
        Instantiates a KeyStruct with a tonic name and tonic pitch class (0-11) and whether it should be major or minor.

        :param tonic_name: the name of the tonic key (use non-ASCII chars for ♭ and ♯)
        :param tonic_pitch_class: the tonic's pitch class, a number from 0 - 11 where 0 = C, 1 = C♯ ... 11 = B
        :param minor: whether this should be minor instead of major, defaults to False.
        """
        validate_pitch_class(tonic_pitch_class)
        self._tonic_pitch_class = tonic_pitch_class

        self._tonic_name = tonic_name
        self._minor = minor
        self._mode = self.MINOR if minor else self.MAJOR

    @property
    def key_name(self):
        """
        Gets the key name as a combo of the tonic name and the mode (a property so can't modify)
        :return: the key name
        """
        return "{} {}".format(self._tonic_name, self._mode)

    @property
    def tonic_pitch_class(self) -> int:
        """
        Gets the tonic pitch class (a property so can't modify)
        :return: the tonic pitch class
        """
        return self._tonic_pitch_class

    def __str__(self) -> str:
        """
        Override built-in to return key_name
        """
        return self.key_name

    def __repr__(self) -> str:
        """
        Override built-in to return key_name
        """
        return self.key_name

    def relative_key_wrt(self, tonic_key: 'KeyStruct') -> str:
        """
        The core method of KeyStruct that allows us to compute the relative key roman numeral for self with
        respect to another KeyStruct that is the tonic_key.

        :param tonic_key: another KeyStruct that is serving as the tonic that we are comparing self to
        :return: a prettified roman numeral string representing the relative key
        """

        # Compute the relative pitch_class by subtracting in modulo-12 arithmetic
        relative_pitch_class = (self.tonic_pitch_class - tonic_key.tonic_pitch_class) % 12
        return RelativeKey.get_relative_key(relative_pitch_class, self._minor)


def validate_is_key_struct(param) -> None:
    """
    Confirms that a given object is a KeyStruct

    :param param: the param to check is a KeyStruct
    :return: nothing if no problems, else raises a TypeError
    """
    if not isinstance(param, KeyStruct):
        raise TypeError("Input '{0}' should be a <class 'KeyStruct>, not a {1}".format(str(param), type(param)))


class Key(object):
    """
    An enum for all 30 (non-double flat or double sharp) keys (leveraging the KeyStructs)
    """
    C_MAJOR = KeyStruct('C', 0)
    C_MINOR = KeyStruct('C', 0, minor=True)

    C_SHARP_MAJOR = KeyStruct('C♯', 1)
    C_SHARP_MINOR = KeyStruct('C♯', 1, minor=True)
    D_FLAT_MAJOR = KeyStruct('D♭', 1)

    D_MAJOR = KeyStruct('D', 2)
    D_MINOR = KeyStruct('D', 2, minor=True)

    D_SHARP_MINOR = KeyStruct('D♯', 3, minor=True)
    E_FLAT_MAJOR = KeyStruct('E♭', 3)
    E_FLAT_MINOR = KeyStruct('E♭', 3, minor=True)

    E_MAJOR = KeyStruct('E', 4)
    E_MINOR = KeyStruct('E', 4, minor=True)

    F_MAJOR = KeyStruct('F', 5)
    F_MINOR = KeyStruct('F', 5, minor=True)

    F_SHARP_MAJOR = KeyStruct('F♯', 6)
    F_SHARP_MINOR = KeyStruct('F♯', 6, minor=True)
    G_FLAT_MAJOR = KeyStruct('G♭', 6)

    G_MAJOR = KeyStruct('G', 7)
    G_MINOR = KeyStruct('G', 7, minor=True)

    G_SHARP_MINOR = KeyStruct('G♯', 8, minor=True)
    A_FLAT_MAJOR = KeyStruct('A♭', 8)
    A_FLAT_MINOR = KeyStruct('A♭', 8, minor=True)

    A_MAJOR = KeyStruct('A', 9)
    A_MINOR = KeyStruct('A', 9, minor=True)

    A_SHARP_MINOR = KeyStruct('A♯', 10, minor=True)
    B_FLAT_MAJOR = KeyStruct('B♭', 10)
    B_FLAT_MINOR = KeyStruct('B♭', 10, minor=True)

    B_MAJOR = KeyStruct('B', 11)
    B_MINOR = KeyStruct('B', 11, minor=True)
    C_FLAT_MAJOR = KeyStruct('C♭', 11)


if __name__ == '__main__':
    print(Key.E_FLAT_MINOR.relative_key_wrt(Key.C_FLAT_MAJOR))
