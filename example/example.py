from __future__ import annotations

import dataclasses

from softboiled import SoftBoiled


@SoftBoiled
@dataclasses.dataclass
class ExampleAPIModel:
    id: int
    name: str
    details: ExampleAPISubModel
    more: bool


@SoftBoiled
@dataclasses.dataclass
class ExampleAPISubModel:
    color: str
    number: int
    true: bool
    size: str


EXAMPLE01 = {
    "id": 1,
    "name": "Example Response v1",
    "details": {"color": "blue", "number": 42, "true": False},
    "more": False,
}

EXAMPLE02 = {
    "id": 1,
    "name": "Example Response v1",
    "status": "depreciated",
    "details": {"color": "blue", "number": 42, "size": "medium"},
    "more": False,
}

valid_model01 = ExampleAPIModel(**EXAMPLE01)
valid_model02 = ExampleAPIModel(**EXAMPLE02)

print(valid_model01)
print(valid_model02)
