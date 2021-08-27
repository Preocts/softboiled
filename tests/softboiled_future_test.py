"""
Tests for ./softboiled/softboiled.py

Trimmed version ensuring __future__ annotations work

Author: Preocts, discord: Preocts#8196
"""
from __future__ import annotations

import dataclasses
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from softboiled import SoftBoiled

INNER_NEST: Dict[str, Any] = {
    "data01": "Hi",
    "data02": True,
    "data03": {"data01": "Norm"},
}

INNER_LIST = [INNER_NEST, INNER_NEST]

JUST_RIGHT: Dict[str, Any] = {
    "tdata01": "This is all",
    "tdata02": INNER_NEST,
    "tdata03": "Why are you still here",
    "tdata04": INNER_LIST,
}


@SoftBoiled
@dataclasses.dataclass
class TopLayerF:
    tdata01: str
    tdata02: NestedLayerF
    tdata03: Optional[str]
    tdata04: Optional[List[NestedLayerF]]


@SoftBoiled
@dataclasses.dataclass
class NestedLayerF:
    data01: Optional[str]
    data02: bool
    data03: NestedNormF


@SoftBoiled
@dataclasses.dataclass
class NestedNormF:
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


def test_just_right_future() -> None:
    """Pass/fail"""
    import logging

    log = logging.getLogger(__name__)
    log.error(SoftBoiled.platter)
    result = TopLayerF(**JUST_RIGHT)

    assert result.tdata01 == JUST_RIGHT["tdata01"]
    assert result.tdata02 == NestedLayerF(**INNER_NEST)
    assert result.tdata03 == JUST_RIGHT["tdata03"]
    assert result.tdata04 == [
        NestedLayerF(**INNER_NEST),
        NestedLayerF(**INNER_NEST),
    ]
