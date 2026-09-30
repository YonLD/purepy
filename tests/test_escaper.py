from pure.core.Escaper import Escaper


def test_text_escapes_the_five_characters_htmlspecialchars_escapes():
    assert Escaper.text("<script>") == "&lt;script&gt;"
    assert Escaper.text("a & b") == "a &amp; b"
    assert Escaper.text('a"b') == "a&quot;b"
    # PHP spells the single quote as a decimal reference.
    assert Escaper.text("a'b") == "a&#039;b"


def test_text_keeps_the_entities_a_value_already_carries():
    # A value that is already escaped is not escaped twice, so markup that was
    # written as entities survives a round trip through a slot.
    assert Escaper.text("&copy; &amp;") == "&copy; &amp;"


def test_text_escapes_an_ampersand_that_names_no_entity():
    # `&notreal;` has the shape of an entity but names nothing, so it is text.
    assert Escaper.text("&notreal;") == "&amp;notreal;"
    assert Escaper.text("& x") == "&amp; x"
    # The table htmlspecialchars() consults is the HTML 4.01 one, so a name that
    # only HTML 5 added is text as well.
    assert Escaper.text("&apos;") == "&amp;apos;"
    assert Escaper.text("&AMP;") == "&amp;AMP;"


def test_an_entity_without_its_semicolon_is_text():
    # A reference a browser cannot terminate is text, and the `&` is escaped.
    assert Escaper.text("&copy") == "&amp;copy"
    assert Escaper.text("&#41") == "&amp;#41"
    assert Escaper.text("&#x41") == "&amp;#x41"


def test_a_numeric_reference_is_kept_across_the_whole_unicode_range():
    # purephp asks only whether the value is a code point, not whether that code
    # point has a character, so both edges are preserved.
    assert Escaper.text("&#0;") == "&#0;"
    assert Escaper.text("&#xD800;") == "&#xD800;"
    assert Escaper.text("&#xFFFE;") == "&#xFFFE;"
    assert Escaper.text("&#x10FFFF;") == "&#x10FFFF;"


def test_a_numeric_reference_past_the_range_is_escaped():
    assert Escaper.text("&#x110000;") == "&amp;#x110000;"
    assert Escaper.text("&#1114112;") == "&amp;#1114112;"
    # Malformed and negative forms are text too.
    assert Escaper.text("&#0x;") == "&amp;#0x;"
    assert Escaper.text("&#;") == "&amp;#;"
    assert Escaper.text("&#-1;") == "&amp;#-1;"


def test_a_placeholder_character_in_the_value_survives():
    # The entities are held aside by position, so a value that contains the
    # character used to mark them keeps that character.
    assert Escaper.text("a\x00b &copy; c") == "a\x00b &copy; c"


def test_attr_double_encodes_the_entities():
    # An attribute may legitimately hold an `&` sequence, so it is escaped even
    # when it looks like an entity.
    assert Escaper.attr("&copy; &amp;") == "&amp;copy; &amp;amp;"
    assert Escaper.attr('a"b') == "a&quot;b"
    assert Escaper.attr("a'b") == "a&#039;b"


def test_attribute_serializes_one_chunk():
    assert Escaper.attribute("class", 'a"b') == ' class="a&quot;b"'


def test_unencodable_input_is_substituted():
    # ENT_SUBSTITUTE replaces what cannot be encoded instead of dropping it.
    assert Escaper.text("a\ud800b") == "a�b"
    assert Escaper.text("a\udc00b") == "a�b"


def test_a_matched_surrogate_pair_substitutes_each_half():
    # PHP holds a string as bytes, so it sees the pair as two invalid three-byte
    # sequences and replaces each one: two U+FFFD, not the character the pair
    # stands for. Keeping the pair would leave a str that cannot be encoded at
    # all, so the output would be unusable.
    assert Escaper.text("a\ud800\udc00b") == "a��b"
    assert Escaper.text("a\ud83d\ude00b") == "a��b"
    # A real astral character is one code point above U+FFFF and passes through.
    assert Escaper.text("a\U0001f600b") == "a\U0001f600b"
    assert Escaper.text("a\U00010000b") == "a\U00010000b"


def test_to_string_renders_a_bool_the_way_the_php_cast_does():
    # `(string)true` is "1" and `(string)false` is "", not the repr. Left to
    # str(), a child would print `True` into the document.
    assert Escaper.to_string(True) == "1"
    assert Escaper.to_string(False) == ""
    assert Escaper.to_string(None) == ""


def test_to_string_renders_a_float_at_the_php_precision():
    # PHP renders a float at `precision=14` in %G notation, so an integral one
    # loses the `.0` that str() would add and a long one is cut to 14 digits.
    assert Escaper.to_string(1.0) == "1"
    assert Escaper.to_string(0.0) == "0"
    assert Escaper.to_string(-1.0) == "-1"
    assert Escaper.to_string(1.5) == "1.5"
    assert Escaper.to_string(-0.0) == "-0"
    assert Escaper.to_string(0.1) == "0.1"
    assert Escaper.to_string(1 / 3) == "0.33333333333333"


def test_to_string_switches_to_an_exponent_outside_the_g_range():
    # %G uses an exponent from 1e14 and below 1e-4, and the cast writes the
    # mantissa with a digit after the point and the exponent unpadded.
    assert Escaper.to_string(99999999999999.0) == "99999999999999"
    assert Escaper.to_string(1e14) == "1.0E+14"
    assert Escaper.to_string(1e15) == "1.0E+15"
    assert Escaper.to_string(1e25) == "1.0E+25"
    assert Escaper.to_string(1e100) == "1.0E+100"
    assert Escaper.to_string(0.001) == "0.001"
    assert Escaper.to_string(0.0001) == "0.0001"
    assert Escaper.to_string(1e-5) == "1.0E-5"
    assert Escaper.to_string(1e-7) == "1.0E-7"


def test_to_string_covers_the_non_finite_floats():
    assert Escaper.to_string(float("inf")) == "INF"
    assert Escaper.to_string(float("-inf")) == "-INF"
    assert Escaper.to_string(float("nan")) == "NAN"


def test_to_string_leaves_a_string_or_an_int_alone():
    assert Escaper.to_string("text") == "text"
    assert Escaper.to_string(0) == "0"
    assert Escaper.to_string(-42) == "-42"
