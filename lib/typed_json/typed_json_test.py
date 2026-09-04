"""Runtime behavior of typed_json (type-level guarantees live in typesafety/)."""

from io import StringIO

from typed_json import dump, dumps, is_json_value, loads


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


class DescribeDumpsOptions:
    def it_forwards_sort_keys(self) -> None:
        assert dumps({"b": 1, "a": 2}, sort_keys=True) == '{"a": 2, "b": 1}'

    def it_forwards_separators(self) -> None:
        assert dumps({"a": 1, "b": 2}, separators=(",", ":")) == '{"a":1,"b":2}'

    def it_forwards_ensure_ascii(self) -> None:
        assert dumps("é", ensure_ascii=False) == '"é"'

    def it_forwards_options_to_dump(self) -> None:
        buffer = StringIO()
        dump({"b": 1, "a": 2}, buffer, sort_keys=True)
        assert buffer.getvalue() == '{"a": 2, "b": 1}'
