# typed-json

stdlib `json.loads`/`dumps`, typed as a recursive `JsonValue` instead of `Any`.

`json.loads` is annotated `-> Any`, which silently switches off type checking
for everything you do with the result. `typed-json` narrows that boundary to
`JsonValue` — a recursive union
(`None | bool | int | float | str | list | dict`) that the type checker can
actually follow — so a single un-typed value can't quietly poison the types
downstream of it.

```python
from typed_json import loads, dumps

value = loads('{"items": [1, 2.5, null]}')   # JsonValue, not Any
text = dumps(value)                           # input constrained to JsonValue
```

## The contract: no `Any`

That's the whole promise — nothing more, nothing less.

- **`loads` / `load`** cast the stdlib result to `JsonValue`. Under the default
  decoder (no custom `parse_*` / `object_hook` settings) `json.loads` provably
  returns a value within `JsonValue`, so the cast is sound at **zero runtime
  cost** — no validation pass.
- **`dumps` / `dump`** accept only `JsonValue`. Because that type is exactly the
  set of natively-serializable values, the checker rejects a `set`/`datetime`
  _statically_, and no `default=` hook is ever needed.

## When stdlib's guarantee doesn't apply: the guards

For a value of genuinely unknown origin — an `object`/`Any` from another
library, a YAML/msgpack/pickle load, hand-built data — cast is _not_ sound.
Reach for the `TypeGuard`s, which validate at runtime by recursing the tree:

```python
from typed_json import is_json_value

def handle(payload: object) -> None:
    if is_json_value(payload):
        reveal_type(payload)  # JsonValue
```

Also available: `is_json_primitive`, `is_json_array`, `is_json_object`.

## Types

`JsonValue`, `JsonPrimitive`, `JsonObject` (`dict[str, JsonValue]`), and
`JsonArray` (`list[JsonValue]`) are exported as PEP 695 type aliases.

## Install

```bash
uv add typed-json   # or: pip install typed-json
```

Requires Python ≥ 3.12 (PEP 695 `type` statements). Zero runtime dependencies.

## License

MIT
