from typing import get_type_hints

from src.entities.states.state_builder import DynamicTypedDictBuilder


def test_create_typeddict_carries_fields():
    td = DynamicTypedDictBuilder.create_typeddict("S", {"a": str, "b": int})
    hints = get_type_hints(td)
    assert hints == {"a": str, "b": int}
    assert td.__name__ == "S"


def test_add_field_returns_extended_copy():
    base = DynamicTypedDictBuilder.create_typeddict("S", {"a": str})
    extended = DynamicTypedDictBuilder.add_field(base, "c", list)
    assert "c" in get_type_hints(extended)
    assert "c" not in get_type_hints(base)
