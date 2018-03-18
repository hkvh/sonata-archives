#!/usr/bin/env python
"""
A class containing all enums related to pitches, keys and relative keys as well as ways to compute them easily.
"""
from typing import Union


class MeasureException(Exception):
    """
    An exception for when a key is invalid
    """


class MeasureRange(object):
    """
    An class for measure number ranges that can also compute measure counts and filter input.
    """

    def __init__(self, start_measure_num: int, end_measure_num: Union[int, None] = None):
        """
            Takes start and end measure numbers and turns them into a MeasureRange.
            If no end_measure included, will assume this is a one bar range with start = end.

            :param start_measure_num: the start measure (inclusive)
            :param end_measure_num: the end measure (inclusive). If None / not included, assumed to = start_measure
            :return: a range string with both start and end measures
            """
        if end_measure_num is None:
            end_measure_num = start_measure_num

        if start_measure_num > end_measure_num:
            raise MeasureException(
                "Start measure {} was greater than end measure {}".format(start_measure_num, end_measure_num))
        self.start_measure_num = start_measure_num
        self.end_measure_num = end_measure_num

    @property
    def count(self) -> int:
        """
        Computes the count of the range, assuming both end points were inclusive, so m. 12 - 14 means count = 3
        :return: the count of measures in the range
        """
        return self.end_measure_num - self.start_measure_num + 1

    def __repr__(self):
        """
        Display the string representation for this range that has different outputs for singlets vs. ranges
        :return: the string repr
        """
        if self.start_measure_num == self.end_measure_num:
            return "m. {}".format(self.start_measure_num)
        return "mm. {} - {}".format(self.start_measure_num, self.end_measure_num)


def validate_is_measure_range(param) -> None:
    """
    Confirms that a given object is a MeasureRange

    :param param: the param to check is a MeasureRange
    :return: nothing if no problems, else raises a TypeError
    """
    if not isinstance(param, MeasureRange):
        raise TypeError("Input '{0}' should be a <class 'MeasureRange>, not a {1}".format(str(param), type(param)))


if __name__ == '__main__':
    print(MeasureRange(204))
    print(MeasureRange(202, 204))
    print(MeasureRange(202, 204).count)
    print(MeasureRange(202, 204).count)