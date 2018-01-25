#!/usr/bin/env python
import time
from functools import wraps
from typing import Callable, Any

import logging


def print_execution_time(description: str = None) -> Callable[..., Any]:
    """
    A decorator with parameter that will print how long a function took to execute
    Uses functools.wraps so that the docstring and name for the function we're decorating is not lost

    :param description: A description of what should be logged
    :return: a wrapper function (of a wrapper function) that starts the clock, runs the original function
    and then logs the time
    """

    def inner(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def __wrapper(*args, **kwargs):
            t0 = time.time()
            result = func(*args, **kwargs)
            print("{0}ompleted in {1:.2f} seconds\n".format(description + " c" if description is not None else "C",
                                                            time.time() - t0))
            return result

        return __wrapper

    return inner


def log_info_execution_time(description: str = None) -> Callable[..., Any]:
    """
    A decorator with parameter that will log how long a function took to execute
    Uses functools.wraps so that the docstring and name for the function we're decorating is not lost

    :param description: A description of what should be logged
    :return: a wrapper function (of a wrapper function) that starts the clock, runs the original function
    and then logs the time
    """

    def inner(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def __wrapper(*args, **kwargs):
            t0 = time.time()
            # Log this to the module the function was defined in, not this module
            log = logging.getLogger(func.__module__)
            result = func(*args, **kwargs)
            log.info("{0}ompleted in {1:.2f} seconds\n".format(description + " c" if description is not None else "C",
                                                               time.time() - t0))
            return result

        return __wrapper

    return inner


@print_execution_time("Foo")
def foo():
    """
    Foo Function
    :return:
    """
    for i in range(10000000):
        i ** 2
    print("Hello")


@log_info_execution_time("Bar")
def bar():
    for i in range(10000000):
        i ** 2
    print("Hello")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)s %(levelname)s: %(message)s')
    foo()
    print(foo.__doc__)
    print(foo.__name__)

    bar()
