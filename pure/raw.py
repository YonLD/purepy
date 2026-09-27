from .core.Raw import Raw


def raw_html(content: str) -> Raw:
    return Raw.of(content)


def raw_xml(content: str) -> Raw:
    return Raw.of(content)
