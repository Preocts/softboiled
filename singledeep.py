"""
The goal here is to create a single deep dataclass that
filters its own parameters on init
"""
from __future__ import annotations

import dataclasses
from typing import Any
from typing import Dict
from typing import Optional
from typing import Type

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


class SafeLoader:
    @staticmethod
    def cleandata(obj: Type, data: Dict[str, Any]) -> Dict[str, Any]:
        """Cleans data, removing keys that are not supported by object"""
        expected = [field.name for field in dataclasses.fields(obj)]
        return {key: value for key, value in data.items() if key in expected}


@dataclasses.dataclass
class SimpleLayer(SafeLoader):
    data01: str = ""
    data02: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> SimpleLayer:
        """create from dict"""
        return cls(**cls.cleandata(SimpleLayer, data))


print("Creating Small")
small = SimpleLayer.from_dict(TOO_SMALL)
print(small)

print("\nCreating Medium")
medium = SimpleLayer.from_dict(JUST_RIGHT)
print(medium)

print("\nCreating Large")
large = SimpleLayer.from_dict(TOO_MUCH)
print(large)
