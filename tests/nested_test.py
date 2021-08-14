from dclearning.nested import NestedLayer
from dclearning.nested import TopLayer

INNER_NEST = {"data01": "There is no more"}

TOO_SMALL = {
    "data01": "This is all",
}

JUST_RIGHT = {
    "data01": "This is all",
    "data02": INNER_NEST,
    "data03": "Why are you still here",
}

TOO_MUCH = {
    "data01": "This is all",
    "data02": "There is no more",
    "data03": "Why are you still here",
    "data04": "Go home",
}


def test_just_right() -> None:
    """Pass/fail"""
    result = TopLayer.from_dict(JUST_RIGHT)

    assert result.data01 == JUST_RIGHT["data01"]
    assert result.data02 == NestedLayer.from_dict(INNER_NEST)
    assert result.data03 == JUST_RIGHT["data03"]
