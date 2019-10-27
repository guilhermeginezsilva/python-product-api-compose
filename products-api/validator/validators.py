import re


def contains_value(list, value) -> bool:
    return value in list


def contains_values(list, values_list):
    return all(elem in list for elem in values_list)


def is_none(value) -> bool:
    if value is None:
        return True
    return False


def in_range(value, min: float, max: float):
    float_value = float(value)
    if min <= float_value <= max:
        return True
    return False


def match(value, regex: str):
    str_value = str(value)
    return re.match(regex, str_value)

