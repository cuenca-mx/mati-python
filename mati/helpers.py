import re


def camel_to_underscore(name) -> str:
    """
    Convert a name from camel case convention to underscore
    lower case convention
    and replace - with _
    Args:
        name (str): name in camel case convention.
    Returns:
        name in underscore lowercase convention.
    """
    camel_regex = re.compile(r'([A-Z])')
    camel_pat = camel_regex.sub(lambda x: '_' + x.group(1).lower(), name)
    return camel_pat.replace("-", "_")


def change_dict_naming_convention(dict_input, convert_function) -> dict:
    """
    Convert a nested dictionary from one convention to another.
    Args:
        dict_input (dict): dictionary (nested or not) to be converted.
        convert_function (func): function that takes the string in one
        convention and returns it in the other one.
    Returns:
        Dictionary with the new keys.
    This code has taken from:
    https://gist.github.com/jllopezpino/132a5cc45ea49f9f8106#file-name_conventions_dictionaries-py
    """
    if not isinstance(dict_input, dict):
        return dict_input
    if isinstance(dict_input, list):
        return dict()  # pragma: no cover
    new = {}
    for k, v in dict_input.items():
        new_v = v
        if isinstance(v, dict):
            new_v = change_dict_naming_convention(v, convert_function)
        elif isinstance(v, list):
            new_v = list()
            for x in v:
                new_v.append(
                    change_dict_naming_convention(x, convert_function)
                )
        new[convert_function(k)] = new_v
    return new
