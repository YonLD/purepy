from typing import Union, Dict, Any, List

def sty(style_dict: Union[Dict[str, Any], None])-> Union[str, None]:
    if not style_dict:
        return None

    style_list: List[str] = []
    for key, val in style_dict.items():
        style_list.append('{}: {}'.format(key, val))

    if not style_list:
        return None
    return '; '.join(style_list) + ';'
