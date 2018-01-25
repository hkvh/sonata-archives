#!/usr/bin/env python
"""
I know the pythonic way with duck typing etc. is to not check for types... but sometimes I really want to
"""
import collections
import numbers
from datetime import timedelta, date as date_type, datetime as datetime_type
from typing import Union


def validate_is_int(param) -> None:
    """
    A function that checks to make sure the type of a parameter is an int.

    :param param: the parameter to check
    :return: nothing if it is some integral subclass or int
    :raises TypeError: if it is not an int
    """
    if not isinstance(param, numbers.Integral):  # this includes int
        raise TypeError(
            "Input '{0}' should be a some instance of a Real number, not a {1}".format(
                str(param), type(param)))


def validate_is_numeric(param) -> None:
    """
    A function that checks to make sure the type of a parameter is a number (not a decimal.Decimal)

    :param param: the parameter to check
    :return: nothing if it is some real number
    :raises TypeError: if it is not an real number
    """
    if not isinstance(param, numbers.Real):  # decimal.Decimal will fail, so you must convert to float
        raise TypeError(
            "Input '{0}' should be a some instance of a real number (i.e. float or an int), not a {1}".format(
                str(param), type(param)))


def validate_is_bool(param) -> None:
    """
    A function that checks to make sure the type of a parameter is bool.

    :param param: the parameter to check
    :return: nothing if it is some boolean
    :raises TypeError: if it is not a boolean
    """
    if not isinstance(param, bool):
        raise TypeError(
            "Input '{0}' should be a an instance of bool, not a {1}".format(
                str(param), type(param)))


def validate_is_str(param) -> None:
    """
    A function that checks to make sure the type of a parameter is string.
    :param param: the parameter to check
    :return: nothing if it is some string
    :raises TypeError: if it is not a string
    """
    if not isinstance(param, str):
        raise TypeError(
            "Input '{0}' should be a an instance of str, not a {1}".format(
                str(param), type(param)))


def validate_is_non_str_iterable(param) -> None:
    """
    A function that checks to make sure the type of a parameter is an iterable but not a string.

    (Note this caveat is because python treats strings as iterable, parsing through their chars, which is something
    that I almost never want)

    :param param: the parameter to check
    :return: nothing if it is some non-string iterable
    :raises TypeError: if it is a string or not an iterable
    """
    if isinstance(param, str) or not isinstance(param, collections.Iterable):
        raise TypeError(
            "Input '{0}' should be a an instance of a non-string iterable, not a {1}".format(
                str(param), type(param)))


def validate_iterable_contains_only_str(param) -> None:
    """
    A function that makes sure an iterable contains only strings

    :param param: the parameter to check
    :return: nothing if every element in the param is a string
    :raises TypeError: if it's not a non-string iterable or any elements in the iterable are not a string
    """
    validate_is_non_str_iterable(param)
    if any([not isinstance(x, str) for x in param]):
        raise TypeError(
            "Input '{0}' should be an iterable with only strings".format(
                str(param), type(param)))


def validate_is_tuple_of_ints(param) -> None:
    """
    A function that checks to make sure the type of a parameter is a tuple of ints.

    :param param: the parameter to check
    :return: nothing if it is some tuple of ints
    :raises TypeError: if it is not a tuple of ints
    """
    if not isinstance(param, tuple):
        raise TypeError(
            "Input '{0}' should be a an instance of tuple, not a {1}".format(
                str(param), type(param)))
    if any([not isinstance(x, numbers.Integral) for x in param]):
        raise TypeError(
            "Input '{0}' should be a tuple with only ints".format(
                str(param), type(param)))


def validate_is_list(param) -> None:
    """
    A function that checks to make sure the type of a parameter is a list

    :param param: the parameter to check
    :return: nothing if it is a list
    :raises TypeError: if it is not a list
    """
    if not isinstance(param, list):
        raise TypeError(
            "Input '{0}' should be a an instance of list, not a {1}".format(
                str(param), type(param)))


def validate_is_dict(param) -> None:
    """
    A function that checks to make sure the type of a parameter is a dict

    :param param: the parameter to check
    :return: nothing if it is a dict
    :raises TypeError: if it is not a dict
    """
    if not isinstance(param, dict):
        raise TypeError(
            "Input '{0}' should be a an instance of dict, not a {1}".format(
                str(param), type(param)))


def day_differ(later_date: Union[datetime_type, date_type], earlier_date: Union[datetime_type, date_type]):
    """
    A function that computes the difference between two datetime.dates in days. Will be positive if later_date is
    after earlier_date, negative otherwise

    :param later_date: the date to subtract the earlier date from (can also be a datetime)
    :param earlier_date: the earlier date (can also be a datetime)
    :return: the integer difference in days
    :raises TypeError: if it is not an instance of datetime.date or its subclass datetime.datetime
    """
    validate_is_date_or_datetime(later_date)
    validate_is_date_or_datetime(earlier_date)
    # Take the day piece of the time_delta
    return (later_date - earlier_date).days


def day_offset(original_date: date_type, num_days: int) -> date_type:
    """
    A function the returns the date that is num_days added to the original_date
    :original_date
    :param original_date the date to add days to (can also be a datetime)
    :param num_days: the number of days to add to the original_date
    :return: the date with that number of days (negative or positive) added to it
    Note that if you give a datetime, the result will remain a datetime, and if you give a date
    the result will remain a date
    :raises TypeError: if it is not an instance of datetime.date
    """
    validate_is_date_or_datetime(original_date)
    return original_date + timedelta(days=num_days)


def validate_is_date(param) -> None:
    """
    A function that checks to make sure the type of a parameter is a datetime.date and also not its subclass
    datetime.datetime

    :param param: the parameter to check
    :return: nothing if it is a datetime.date
    :raises TypeError: if it is not an instance of datetime.date or if it is its subclass datetime.datetime
    """
    if not isinstance(param, date_type) or isinstance(param, datetime_type):
        raise TypeError("Input '{0}' should be a <class 'datetime.date'>, not a {1}".format(str(param), type(param)))


def validate_is_datetime(param) -> None:
    """
    A function that checks to make sure the type of a parameter is a datetime.datetime

    :param param: the parameter to check
    :return: nothing if it is a datetime.datetime
    :raises TypeError: if it is not a datetime.datetime
    """
    if not isinstance(param, datetime_type):
        raise TypeError(
            "Input '{0}' should be a <class 'datetime.datetime'>, not a {1}".format(str(param), type(param)))


def validate_is_date_or_datetime(param) -> None:
    """
    A function that checks to make sure the type of a parameter is a datetime.date and its subclass datetime.datetime
    (which is a subclass of it)

    :param param: the parameter to check
    :return: nothing if it is a datetime.date
    :raises TypeError: if it is not an instance of datetime.date
    """
    if not isinstance(param, date_type):  # this includes datetime.datetime
        raise TypeError(
            "Input '{0}' should be a <class 'datetime.date'> or <class 'datetime.datetime'>, not a {1}".format(
                str(param), type(param)))


if __name__ == '__main__':
    validate_is_int(4)
    # validate_is_bool(None)
    # validate_is_bool("True")
    validate_is_bool(True)
    validate_is_numeric(2)
    validate_is_tuple_of_ints((2,))
