"""
The goal here is to create a single deep dataclass that
filters its own parameters on init
"""
from singledeep import SimpleLayer

TOO_SMALL = {"data01": "This is all"}

JUST_RIGHT = {
    "data01": "This is all",
    "data02": "There is no more",
}

TOO_MUCH = {
    "data01": "This is all",
    "data02": "There is no more",
    "data03": "Why are you still here",
}


def test_too_small() -> None:
    """Pass/fail"""
    SimpleLayer.from_dict(TOO_SMALL)


def test_just_right() -> None:
    """Pass/fail"""
    SimpleLayer.from_dict(JUST_RIGHT)


def test_too_large() -> None:
    """Pass/fail"""
    SimpleLayer.from_dict(TOO_MUCH)
