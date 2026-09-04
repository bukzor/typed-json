"""Typed JSON: stdlib `json` without `Any` contamination.

The stdlib `json.loads` returns `Any`, which silently switches off type
checking for everything downstream. This package narrows the JSON boundary to
`JsonValue` — a recursive union the type checker can actually follow.

Two tools, for two situations:

- `loads`/`load`/`dumps`/`dump` mirror their stdlib counterparts but in terms of
  `JsonValue`. Under the default decoder (no custom `parse_*`/`object_hook`
  settings), `json.loads` provably returns a value within `JsonValue`, so
  `loads` *casts* — sound, at zero runtime cost. On the write side the input
  type guarantees serializability, so no `default=` hook is ever needed.

- `is_json_value` (and friends) validate at runtime via `TypeGuard`. Reach for
  these only when a value's origin is genuinely unknown — an `object`/`Any` from
  another library, a YAML/msgpack/pickle load, hand-built data — where the
  stdlib guarantee does not apply.

The `# pyright: ignore` lines in the guards are unavoidable: `isinstance`
narrows `object` to `list`/`dict` with *unknown* element types — exactly what
the recursion exists to pin down.
"""

import json
from typing import IO, TypeGuard, cast

type JsonPrimitive = None | bool | int | float | str
type JsonValue = JsonPrimitive | JsonArray | JsonObject
type JsonObject = dict[str, JsonValue]
type JsonArray = list[JsonValue]

__all__ = [
    "JsonPrimitive",
    "JsonValue",
    "JsonObject",
    "JsonArray",
    "loads",
    "load",
    "dumps",
    "dump",
    "is_json_primitive",
    "is_json_array",
    "is_json_object",
    "is_json_value",
]


def loads(s: str | bytes | bytearray) -> JsonValue:
    """Parse JSON text, typed as `JsonValue` instead of `Any`.

    >>> loads('{"a": [1, 2.5, null]}')
    {'a': [1, 2.5, None]}
    """
    return cast(JsonValue, json.loads(s))


def load(fp: IO[str] | IO[bytes]) -> JsonValue:
    """Read and parse JSON from a file, typed as `JsonValue` instead of `Any`."""
    return cast(JsonValue, json.load(fp))


def dumps(
    obj: JsonValue,
    *,
    skipkeys: bool = False,
    ensure_ascii: bool = True,
    check_circular: bool = True,
    allow_nan: bool = True,
    indent: int | str | None = None,
    separators: tuple[str, str] | None = None,
    sort_keys: bool = False,
) -> str:
    """Serialize a `JsonValue` to text. The input type guarantees serializability.

    Every stdlib formatting option is forwarded except `cls` and `default`, which
    are the two that would hand the encoder a value outside `JsonValue` -- the
    guarantee this module exists to keep.

    >>> dumps({"a": [1, None]})
    '{"a": [1, null]}'
    >>> dumps({"b": 1, "a": 2}, sort_keys=True)
    '{"a": 2, "b": 1}'
    """
    return json.dumps(
        obj,
        skipkeys=skipkeys,
        ensure_ascii=ensure_ascii,
        check_circular=check_circular,
        allow_nan=allow_nan,
        indent=indent,
        separators=separators,
        sort_keys=sort_keys,
    )


def dump(
    obj: JsonValue,
    fp: IO[str],
    *,
    skipkeys: bool = False,
    ensure_ascii: bool = True,
    check_circular: bool = True,
    allow_nan: bool = True,
    indent: int | str | None = None,
    separators: tuple[str, str] | None = None,
    sort_keys: bool = False,
) -> None:
    """Serialize a `JsonValue` to a file. The input type guarantees serializability.

    Options forward as in `dumps`, with `cls` and `default` withheld for the
    same reason.
    """
    json.dump(
        obj,
        fp,
        skipkeys=skipkeys,
        ensure_ascii=ensure_ascii,
        check_circular=check_circular,
        allow_nan=allow_nan,
        indent=indent,
        separators=separators,
        sort_keys=sort_keys,
    )


def is_json_primitive(value: object) -> TypeGuard[JsonPrimitive]:
    """Whether `value` is a JSON primitive (`None`/`bool`/`int`/`float`/`str`)."""
    return value is None or isinstance(value, (bool, int, float, str))


def is_json_array(value: object) -> TypeGuard[JsonArray]:
    """Whether `value` is a `list` whose every element is a `JsonValue`."""
    return isinstance(value, list) and all(
        is_json_value(v)  # pyright: ignore[reportUnknownArgumentType]
        for v in value  # pyright: ignore[reportUnknownVariableType]
    )


def is_json_object(value: object) -> TypeGuard[JsonObject]:
    """Whether `value` is a `dict` with `str` keys and `JsonValue` values."""
    if not isinstance(value, dict):
        return False
    return all(
        isinstance(k, str)
        and is_json_value(v)  # pyright: ignore[reportUnknownArgumentType]
        for k, v in value.items()  # pyright: ignore[reportUnknownVariableType]
    )


def is_json_value(value: object) -> TypeGuard[JsonValue]:
    """Whether `value` is a `JsonValue`, recursing through arrays and objects.

    >>> is_json_value({"a": [1, None, "x"]})
    True
    >>> is_json_value({1, 2})
    False
    """
    return is_json_primitive(value) or is_json_array(value) or is_json_object(value)
