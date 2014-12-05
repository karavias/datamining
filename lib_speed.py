"""
lib_speed module.

This module creates decorators and functions used to calculate
the performance of functions.
"""

from functools import wraps
import time
from pandas import DataFrame, Series

#the dictionary that holds the measures
SPEED_SCORES = {}

def speed_calculate(func):
    """Add the performance score of a function to the dictionary."""
    @wraps(func)
    def inner(*args, **kwargs):
        """Wrap and execute the decorated function."""
        start = time.time()
        result = func(*args, **kwargs) #2
        if func.__name__ in SPEED_SCORES:
            SPEED_SCORES[func.__name__] = (SPEED_SCORES[func.__name__][0] \
                                        + time.time() - start,\
                                            SPEED_SCORES[func.__name__][1] + 1)
        else:
            SPEED_SCORES[func.__name__] = (time.time() - start, 1)
        return result
    return inner

def reset_calculate(func):
    """Reset calculations before this function starts."""
    @wraps(func)
    def inner(*args, **kwargs):
        """wrap and execute the decorated function."""
        SPEED_SCORES.clear()
        result = func(*args, **kwargs) #2
        return result
    return inner

def get_speed_means():
    """
    Retrieve the mean scores from calculations.

    This should be done before a reset_calculate function finishes.
    Returns the mean scores in HTML-ready table representation.
    """
    data = {}
    for key, item in SPEED_SCORES.iteritems():
        data[key] = Series([item[0]/item[1]],\
            index=["Average time"])
    return DataFrame(data).T.to_html(escape=False)

