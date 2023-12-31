from typing import Union, Dict, Any, List

def clx(*args: Union[Dict[str, Any], str, None, List[Union[str, None]]])-> Union[str, None]:
    arg_list = list(args)
    if not arg_list:
        return None

    class_list: List[str] = []
    for class_name in arg_list:
        if bool(class_name) == False:
            continue
        if isinstance(class_name, str):
            class_list.append(class_name)
            continue
        if isinstance(class_name, dict):
            class_list = class_list + __filterClassList(class_name)
            continue
        if isinstance(class_name, list):
            class_list = class_list + [x for x in class_name if isinstance(x, str) and bool(x)]

    if not class_list:
        return None
    return ' '.join(class_list)


def __filterClassList(class_dict: Dict[str, Any]):
    class_list = [];

    for key, val in class_dict.items():
        if (isinstance(key, str) and bool(key) and bool(val)):
            class_list.append(key)

    return class_list
