"""
Tests for ./softboiled/softboiled.py

Author: Preocts, discord: Preocts#8196
"""
import dataclasses
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

import pytest
from softboiled import SoftBoiled

INNER_NEST_SMALL: Dict[str, Any] = {"data01": "Hi"}
INNER_NEST: Dict[str, Any] = {
    "data01": "Hi",
    "data02": True,
    "data03": {"data01": "Norm"},
}
INNER_NEST_LARGE: Dict[str, Any] = {
    "data01": "Hi",
    "data02": True,
    "data03": {"data01": "Norm"},
    "data04": "wut",
}

INNER_LIST = [INNER_NEST, INNER_NEST]

JUST_RIGHT: Dict[str, Any] = {
    "tdata01": "This is all",
    "tdata02": INNER_NEST,
    "tdata03": "Why are you still here",
    "tdata04": INNER_LIST,
}

TOO_MUCH: Dict[str, Any] = {
    "tdata01": "This is all",
    "tdata02": INNER_NEST,
    "tdata03": "Why are you still here",
    "tdata04": [INNER_NEST_LARGE, INNER_NEST_LARGE],
    "tdata05": "wut",
}

TOO_SMALL: Dict[str, Any] = {
    "tdata04": [INNER_NEST_SMALL, INNER_NEST_SMALL],
}


@SoftBoiled
@dataclasses.dataclass
class TopLayer:
    tdata01: str
    tdata02: "NestedLayer"
    tdata03: Optional[str]
    tdata04: Optional[List["NestedLayer"]]


@SoftBoiled
@dataclasses.dataclass
class NestedLayer:
    data01: Optional[str]
    data02: bool
    data03: "NestedNorm"


@SoftBoiled
@dataclasses.dataclass
class NestedNorm:
    data01: str = ""


DEFAULT_EXPECTED: Dict[str, Any] = {
    "data01": "Test 01",
    "data02": True,
    "data03": 0,
}


@SoftBoiled
@dataclasses.dataclass
class DefaultValues:
    data01: str = DEFAULT_EXPECTED["data01"]
    data02: bool = DEFAULT_EXPECTED["data02"]
    data03: int = DEFAULT_EXPECTED["data03"]


def test_not_a_dataclass() -> None:
    """We don't serve your kind here (EAFP)"""
    with pytest.raises(ValueError):

        @SoftBoiled
        class NotADataClass:
            ...


def test_registered() -> None:
    _ = TopLayer(**JUST_RIGHT)

    assert "TopLayer" in SoftBoiled.platter
    assert "NestedLayer" in SoftBoiled.platter


def test_too_small_missing_all(caplog: Any) -> None:
    """Pass/fail"""
    result = TopLayer()  # type: ignore

    assert result.tdata01 is None

    assert "Type Warning: required key missing" in caplog.text


def test_too_small_with_nest(caplog: Any) -> None:
    """Pass/fail"""
    result = TopLayer(**TOO_SMALL)

    assert result.tdata01 is None
    assert result.tdata02 is None
    assert result.tdata03 is None
    assert result.tdata04 == [
        NestedLayer(**INNER_NEST_SMALL),
        NestedLayer(**INNER_NEST_SMALL),
    ]

    assert "Type Warning: required key missing" in caplog.text


def test_just_right() -> None:
    """Pass/fail"""
    result = TopLayer(**JUST_RIGHT)

    assert result.tdata01 == JUST_RIGHT["tdata01"]
    assert result.tdata02 == NestedLayer(**INNER_NEST)
    assert result.tdata03 == JUST_RIGHT["tdata03"]
    assert result.tdata04 == [
        NestedLayer(**INNER_NEST),
        NestedLayer(**INNER_NEST),
    ]


def test_too_large() -> None:
    """Pass/fail"""
    result = TopLayer(**TOO_MUCH)

    assert result.tdata01 == JUST_RIGHT["tdata01"]
    assert result.tdata02 == NestedLayer(**INNER_NEST_LARGE)
    assert result.tdata03 == JUST_RIGHT["tdata03"]
    assert result.tdata04 == [
        NestedLayer(**INNER_NEST_LARGE),
        NestedLayer(**INNER_NEST_LARGE),
    ]


def test_default_values() -> None:
    """Pass/Fail"""
    result = DefaultValues()

    assert result.data01 == DEFAULT_EXPECTED["data01"]
    assert result.data02 == DEFAULT_EXPECTED["data02"]
    assert result.data03 == DEFAULT_EXPECTED["data03"]


def test_set_values_over_default() -> None:
    """Pass/fail"""
    result = DefaultValues(data01="Hello", data02=False, data03=10)

    assert result.data01 == "Hello"
    assert result.data02 is False
    assert result.data03 == 10
