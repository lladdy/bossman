import json
import os

import numpy as np


def floor(array: np.array, precision=0):
    # https://stackoverflow.com/questions/58065055/floor-and-ceil-with-number-of-decimals
    return np.true_divide(np.floor(array * 10**precision), 10**precision)


def fix_p(p):
    if p.sum() != 1.0:
        p = p * (1.0 / p.sum())
    return p


def ensure_file_dir_exists(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)


def save_json_to_file(file, content):
    ensure_file_dir_exists(file)
    with open(file, "w") as f:
        json.dump(content, f)


def read_decision_context(source_dict, context: dict):
    """
    Reads a value from a variably deep nested entry in a dictionary.
    Inspired by https://stackoverflow.com/questions/3232943/update-value-of-a-nested-dictionary-of-varying-depth
    """
    if len(context) == 0:  # no context
        return source_dict

    key, val = list(context.items())[0]

    if len(context) > 1:  # there are more keys
        new_context = dict(context)
        del new_context[key]
        return read_decision_context(source_dict[key][val], new_context)
    else:
        return source_dict[key][val]


def populate_missing_decision_context_keys(source_dict, context: dict):
    insert_decision_context(source_dict, context)


def insert_decision_context(source_dict: dict, context: dict, value=None):
    """
    Inserts a value into a variably deep nested entry in a dictionary, creating all required keys along the way.
    Inspired by https://stackoverflow.com/questions/3232943/update-value-of-a-nested-dictionary-of-varying-depth

    Call with value=None to simply populate context keys.
    """
    if len(context) == 0:  # no context
        if value is not None:  # if there's a value, update the root dict
            if "choices" not in source_dict:
                source_dict["choices"] = {}
            source_dict["choices"].update(value)
        return

    key, val = list(context.items())[0]

    if key not in source_dict:
        source_dict[key] = {}

    if val not in source_dict[key]:
        source_dict[key][val] = {}

    if len(context) > 1:  # there are more keys
        new_context = dict(context)
        del new_context[key]
        insert_decision_context(source_dict[key][val], new_context, value)
    else:
        if "choices" not in source_dict[key][val]:
            source_dict[key][val]["choices"] = {}
        source_dict[key][val]["choices"] = value or source_dict[key][val]["choices"]
