"""
The goal here is to create a single deep dataclass that
filters its own parameters on init
"""
from typing import Any

from single import SimpleLayer

TOO_SMALL = {
    "data01": "This is all",
}

JUST_RIGHT = {
    "data01": "This is all",
    "data02": "There is no more",
    "data03": "Why are you still here",
}

TOO_MUCH = {
    "data01": "This is all",
    "data02": "There is no more",
    "data03": "Why are you still here",
    "data04": "Go home",
}


def test_too_small(caplog: Any) -> None:
    """Pass/fail"""
    result = SimpleLayer.from_dict(TOO_SMALL)

    assert result.data01 == TOO_SMALL["data01"]
    assert result.data02 is None
    assert result.data03 is None

    assert "Type Warning: required key missing" in caplog.text


def test_just_right() -> None:
    """Pass/fail"""
    result = SimpleLayer.from_dict(JUST_RIGHT)

    assert result.data01 == JUST_RIGHT["data01"]
    assert result.data02 == JUST_RIGHT["data02"]
    assert result.data03 == JUST_RIGHT["data03"]


def test_too_large() -> None:
    """Pass/fail"""
    result = SimpleLayer.from_dict(TOO_MUCH)

    assert result.data01 == JUST_RIGHT["data01"]
    assert result.data02 == JUST_RIGHT["data02"]
    assert result.data03 == JUST_RIGHT["data03"]
