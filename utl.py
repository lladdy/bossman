from typing import List

import numpy as np


def floor(array: np.array, precision=0):
    # https://stackoverflow.com/questions/58065055/floor-and-ceil-with-number-of-decimals
    return np.true_divide(np.floor(array * 10 ** precision), 10 ** precision)


def fix_p(p):
    if p.sum() != 1.0:
        p = p * (1. / p.sum())
    return p


def deep_dict_read(source_dict, keys: List) -> dict:
    """
    Reads a value from a variably deep nested entry in a dictionary.
    Inspired by https://stackoverflow.com/questions/3232943/update-value-of-a-nested-dictionary-of-varying-depth
    """
    assert len(keys) > 0

    current_key = keys[0]
    del keys[0]  # remove the current key

    if len(keys) > 0:  # there are more keys
        return deep_dict_read(source_dict[current_key], keys)
    else:
        return source_dict[current_key]


def deep_dict_insert(source_dict, keys: List, value) -> dict:
    """
    Updates a variably deep nested entry in a dictionary.
    If the keys don't exist, they are created in the order listed.
    Inspired by https://stackoverflow.com/questions/3232943/update-value-of-a-nested-dictionary-of-varying-depth
    """
    assert len(keys) > 0

    current_key = keys[0]
    del keys[0]  # remove the current key

    if current_key not in source_dict:
        source_dict[current_key] = {}

    if len(keys) > 0:  # there are more keys
        source_dict[current_key] = deep_dict_insert(source_dict[current_key], keys, value)
    else:
        source_dict[current_key] = value

    return source_dict
