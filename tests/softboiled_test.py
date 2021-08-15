from __future__ import annotations

import dataclasses
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from softboiled import SoftBoiled

INNER_NEST_SMALL = {"data01": "Hi"}
INNER_NEST = {"data01": "Hi", "data02": True, "data03": {"data01": "Norm"}}
INNER_NEST_LARGE = {
    "data01": "Hi",
    "data02": True,
    "data03": {"data01": "Norm"},
    "data04": "wut",
}

INNER_LIST = [INNER_NEST, INNER_NEST]

JUST_RIGHT: Dict[str, Any] = {
    "data01": "This is all",
    "data02": INNER_NEST,
    "data03": "Why are you still here",
    "data04": INNER_LIST,
}

TOO_MUCH: Dict[str, Any] = {
    "data01": "This is all",
    "data02": INNER_NEST,
    "data03": "Why are you still here",
    "data04": [INNER_NEST_LARGE, INNER_NEST_LARGE],
    "data05": "wut",
}

TOO_SMALL: Dict[str, Any] = {
    "data04": [INNER_NEST_SMALL, INNER_NEST_SMALL],
}


@dataclasses.dataclass
class TopLayer(SoftBoiled):
    data01: str
    data02: NestedLayer
    data03: Optional[str]
    data04: Optional[List[NestedLayer]]

    @classmethod
    def sbload(cls, data: Dict[str, Any]) -> TopLayer:
        """create from dict"""
        return cls(**cls.cleandata(TopLayer, data))


@dataclasses.dataclass
class NestedLayer(SoftBoiled):
    data01: Optional[str]
    data02: bool
    data03: NestedNorm

    @classmethod
    def sbload(cls, data: Dict[str, Any]) -> NestedLayer:
        """create from dict"""
        return cls(**cls.cleandata(NestedLayer, data))


@dataclasses.dataclass
class NestedNorm:
    data01: str = ""


def test_too_small_missing_all(caplog: Any) -> None:
    """Pass/fail"""
    result = TopLayer.sbload({})

    assert result.data01 is None

    assert "Type Warning: required key missing" in caplog.text


def test_too_small_with_nest(caplog: Any) -> None:
    """Pass/fail"""
    result = TopLayer.sbload(TOO_SMALL)

    assert result.data01 is None
    assert result.data02 is None
    assert result.data03 is None
    assert result.data04 == [
        NestedLayer.sbload(INNER_NEST_SMALL),
        NestedLayer.sbload(INNER_NEST_SMALL),
    ]

    assert "Type Warning: required key missing" in caplog.text


def test_just_right() -> None:
    """Pass/fail"""
    result = TopLayer.sbload(JUST_RIGHT)

    assert result.data01 == JUST_RIGHT["data01"]
    assert result.data02 == NestedLayer.sbload(INNER_NEST)
    assert result.data03 == JUST_RIGHT["data03"]
    assert result.data04 == [
        NestedLayer.sbload(INNER_NEST),
        NestedLayer.sbload(INNER_NEST),
    ]


def test_too_large() -> None:
    """Pass/fail"""
    result = TopLayer.sbload(TOO_MUCH)

    assert result.data01 == JUST_RIGHT["data01"]
    assert result.data02 == NestedLayer.sbload(INNER_NEST_LARGE)
    assert result.data03 == JUST_RIGHT["data03"]
    assert result.data04 == [
        NestedLayer.sbload(INNER_NEST_LARGE),
        NestedLayer.sbload(INNER_NEST_LARGE),
    ]
