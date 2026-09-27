from typing import Union, Dict, Any, List


def _number(value) -> str:
    """Render a number the way PHP's string cast does.

    PHP prints 0.0 as "0"; Python's str() would give "0.0".
    """
    if isinstance(value, float) and value.is_integer():
        return str(int(value))

    return str(value)


def _truthy(value) -> bool:
    """PHP's empty() semantics, which purephp's clx() relies on.

    PHP treats '0' and 0 as falsy; Python treats '0' as truthy, so a plain
    truthiness test would keep class names purephp drops.
    """
    if value is None or value is False:
        return False
    if isinstance(value, (int, float)) and value == 0:
        return False
    if isinstance(value, str) and value in ("", "0"):
        return False
    if isinstance(value, (list, dict, tuple, set)) and len(value) == 0:
        return False
    return True


def clx(
    *args: Union[Dict[str, Any], str, int, float, bool, None, List[Any]]
) -> Union[str, None]:
    class_list: List[str] = []

    for class_name in args:
        if isinstance(class_name, list):
            for item in class_name:
                # bool is a subclass of int in Python; purephp drops it because
                # a boolean is not a string and not numeric.
                if isinstance(item, bool):
                    continue
                if isinstance(item, str) and item != "":
                    class_list.append(item)
                elif isinstance(item, (int, float)):
                    class_list.append(_number(item))
            continue

        if isinstance(class_name, dict):
            for key, val in class_name.items():
                if not isinstance(key, str):
                    continue

                # PHP turns a numeric-string array key into an int, so '0' => x
                # is a list entry, judged by its value rather than kept as a key.
                if key.lstrip("-").isdigit():
                    if isinstance(val, bool):
                        continue
                    if isinstance(val, str) and val != "":
                        class_list.append(val)
                    elif isinstance(val, (int, float)):
                        class_list.append(_number(val))
                    continue

                if key != "" and _truthy(val):
                    class_list.append(key)
            continue

        if class_name is None or isinstance(class_name, bool) or class_name == "":
            continue

        if isinstance(class_name, str):
            class_list.append(class_name)
        elif isinstance(class_name, (int, float)):
            class_list.append(_number(class_name))

    if not class_list:
        return None
    return " ".join(class_list)
