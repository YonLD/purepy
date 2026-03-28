from enum import Enum


class RawType(Enum):
    HTML = "HTML"
    XML = "XML"


class Raw:
    def __init__(self, type: RawType, content: str):
        self.__type = type
        self.__content = content

    def __str__(self) -> str:
        return self.__content

    def to_JSON(self):
        return {"type": self.__type.value, "content": self.__content}
