from typing import Any

from dclearning.nested import NestedLayer
from dclearning.nested import NotDC
from dclearning.nested import TopLayer

NAMED_TUPLE = NotDC("It's all objects")
INNER_NEST = {"data01": "There is no more"}

TOO_SMALL = {
    "data02": INNER_NEST,
}

JUST_RIGHT = {
    "data01": "This is all",
    "data02": INNER_NEST,
    "data03": "Why are you still here",
    "data04": NAMED_TUPLE,
}

TOO_MUCH = {
    "data01": "This is all",
    "data02": INNER_NEST,
    "data03": "Why are you still here",
    "data04": "Go home",
}


def test_too_small_missing_all(caplog: Any) -> None:
    """Pass/fail"""
    result = TopLayer.from_dict({})

    assert result.data02 is None

    assert "Type Warning: required key missing" in caplog.text


def test_too_small_with_nest(caplog: Any) -> None:
    """Pass/fail"""
    result = TopLayer.from_dict(TOO_SMALL)

    assert result.data01 is None
    assert result.data02 == NestedLayer.from_dict(INNER_NEST)
    assert result.data03 is None

    assert "Type Warning: required key missing" in caplog.text


def test_just_right() -> None:
    """Pass/fail"""
    result = TopLayer.from_dict(JUST_RIGHT)

    assert result.data01 == JUST_RIGHT["data01"]
    assert result.data02 == NestedLayer.from_dict(INNER_NEST)
    assert result.data03 == JUST_RIGHT["data03"]
    assert result.data04 == NAMED_TUPLE


def test_too_large() -> None:
    """Pass/fail"""
    result = TopLayer.from_dict(TOO_MUCH)

    assert result.data01 == JUST_RIGHT["data01"]
    assert result.data02 == NestedLayer.from_dict(INNER_NEST)
    assert result.data03 == JUST_RIGHT["data03"]
