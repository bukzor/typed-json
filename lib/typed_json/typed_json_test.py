"""Runtime behavior of typed_json (type-level guarantees live in typesafety/)."""

from typed_json import dumps, is_json_value, loads


class DescribeLoadsDumpsRoundTrip:
    def it_round_trips_each_json_shape(self) -> None:
        for text in ("null", "true", "42", "2.5", '"s"', "[1, 2]", '{"a": 1}'):
            assert dumps(loads(text)) == text

    def it_parses_nested_structures(self) -> None:
        assert loads('{"a": [1, {"b": null}]}') == {"a": [1, {"b": None}]}


class DescribeIsJsonValue:
    def it_accepts_nested_json(self) -> None:
        assert is_json_value({"a": [1, 2.5, None, "x", True]})

    def it_rejects_non_json_leaves(self) -> None:
        assert not is_json_value({1, 2})
        assert not is_json_value({"a": {1, 2}})
        assert not is_json_value([object()])

    def it_rejects_non_string_keys(self) -> None:
        assert not is_json_value({1: "a"})
