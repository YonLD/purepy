from .core.Raw import Raw, RawType

def raw_html(content: str):
    return Raw(RawType.HTML, content)

def raw_xml(content: str):
    return Raw(RawType.XML, content)
