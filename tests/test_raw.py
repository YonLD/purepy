from pure.core.Raw import Raw


def test_raw_value_is_publicly_readable():
    raw = Raw.of("<b>x</b>")

    assert isinstance(raw, Raw)
    assert raw.value == "<b>x</b>"


def test_raw_content_is_emitted_verbatim():
    assert str(Raw.of("<b>x</b>")) == "<b>x</b>"
    assert str(Raw.of("<x/>")) == "<x/>"
