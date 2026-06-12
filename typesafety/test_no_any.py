"""Type-level contract for typed_json, verified by pytest-pyright.

Each `# E:` line asserts pyright emits exactly that error on that line; lines
without one must type-check clean. Positive checks use `assert_type` (a runtime
no-op). The one operation that also raises at runtime is wrapped in
`pytest.raises`, so every `it_` here doubles as an ordinary passing test.
"""

from typing import assert_type

import pytest

from typed_json import JsonValue, dumps, loads


class DescribeLoads:
    def it_decodes_to_jsonvalue_not_any(self) -> None:
        # Were the result Any, this would fail: Any is not JsonValue.
        assert_type(loads("{}"), JsonValue)

    def it_is_not_assignable_to_str(self) -> None:
        _s: str = loads("{}")  # E: Type "JsonValue" is not assignable to declared type "str"


class DescribeDumps:
    def it_rejects_non_json_input(self) -> None:
        with pytest.raises(TypeError):
            dumps({1, 2, 3})  # E: Argument of type "set[int]" cannot be assigned to parameter "obj" of type "JsonValue" in function "dumps"
