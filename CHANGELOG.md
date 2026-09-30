# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.1.0] - 2026-09-29

This release brings purepy to behavioural parity with purephp 1.1.0. Every
change below was verified by rendering the same inputs through both
implementations and diffing the bytes.

### Added

- `Escaper.to_string()` coerces a value to text the way purephp's `(string)`
  cast does, and every point where a value becomes text now goes through it: a
  tag child, an attribute value, a slot value, a raw slot element and a
  compiled default. Python's `str()` disagreed with the cast on the two types a
  template actually receives, so `div(active)` printed `True` and `div(1.0)`
  printed `1.0`.
- `Escaper.debug_type()` names a value's type the way PHP's `get_debug_type()`
  does, so a rejected value is reported as `null`, `string` or `array` rather
  than `NoneType`, `str` or `list`. Four messages that reported `list` or `str`
  asserted the old wording and now assert the one purephp prints.
- A tag class builds an element by reading its name, which is what purephp
  reaches through `__callStatic`: `HTML.div('x')`, `SVG.circle(...)` and
  `XML.row(...)` build the same element the module-level functions do, and a
  custom element such as `HTML.myWidget('x')` needs no declaration.
- `RendererCache.prepare()` rejects a cache directory owned by another user. A
  private mode is no protection there: the owner can replace what is inside it
  between two compiles.

### Fixed

- A float reaches a document the way the `(string)` cast writes it: at PHP's
  `precision=14` in `%G` notation, so `1.0` is `1`, `1e15` is `1.0E+15` and
  `1e-7` is `1.0E-7`. The last case is one class of value where the two differ
  — a double needing more than 14 significant digits whose 14-digit rounding
  ends in a zero — and it is documented on `Escaper.to_string()`.
- A plain view writes an attribute value as an echo, the way a hand-written view
  does, so `Slot.value()` in attribute position is cast rather than turned into
  a bare name. The compiled renderer still writes `disabled="disabled"`, which
  is the difference purephp makes between `PlainGenerator` and
  `SlotRuntime::attrOpen()`.
- `SlotRuntime.items()` accepts any iterable rather than only a list or a tuple,
  which is what `is_iterable()` does, and a mapping yields its values the way
  iterating the equivalent PHP array does.
- A `null` child or each value is reported by `scope()` / `items()` — `slot
  'items' must be iterable, null given.` — instead of as a missing slot. Only a
  missing key is the missing-slot error, matching the key-presence rule
  `RendererGenerator::valueAccess()` applies to those two kinds.
- The markup-in-shape error carries the sentence purephp prints, naming the raw
  slot to render the call into.

### Removed

- Five sites that nothing reached and purephp has no counterpart for: the
  `Dom` base class exported from `pure.core`, `Tag.set_attr_by_cb()`,
  `CompileException.missing_slot()`, `PlainGenerator.document()` and
  `ShapeGuard._local()`.

## [1.0.2]

### Added

- The bootstrap, event-counter and XML examples, ported from purephp with the
  same layout, and each given a front controller that serves its directory over
  HTTP (`python3 examples/<name>/public/index.py --serve`) and prints one page
  on stdout (`python3 examples/<name>/public/index.py /plain`).

### Fixed

- The examples were consolidated into the three that purephp ships. The earlier
  `bootstrap_cover`, `bootstrap_features`, `bootstrap_pricing` and
  `event_counter` directories and their `server.py` are gone; their content was
  covered by the new `bootstrap`.
- The examples' own import paths, so a controller resolves a view by path the
  way purephp `require`s it rather than through a package-relative import that
  could not resolve.
- `app/bootstrap.py` calls the generated `view()` rather than looking for a
  `render()` the artifact never defines.
