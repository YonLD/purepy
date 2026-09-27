from typing import Union, Dict, Any, List


def sty(style_dict: Union[Dict[str, Any], None]) -> Union[str, None]:
    if not style_dict:
        return None

    style_list: List[str] = []
    for key, val in style_dict.items():
        # bool is a subclass of int in Python, so it has to be excluded
        # explicitly: purephp drops it because false is not numeric.
        if not isinstance(key, str):
            continue
        if isinstance(val, bool):
            continue
        if isinstance(val, (str, int, float)):
            style_list.append("{}: {}".format(key, val))

    if not style_list:
        return None
    return "; ".join(style_list) + ";"
