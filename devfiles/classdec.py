"""
Decorate a class, return a dataclass
"""
from __future__ import annotations

import dataclasses
import functools
from typing import Any
from typing import List
from typing import Type


class SoftBoiled:
    registered_classes: List[str] = []

    def __init__(self, cls: Type[Any]) -> None:
        self.cls = cls
        SoftBoiled.registered_classes.append(cls.__name__)
        functools.update_wrapper(self, cls)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self.cls(*args, **kwargs)


@SoftBoiled
@dataclasses.dataclass
class ProtoType:
    data01: str
    data02: str


my_dc = ProtoType("check", "out")
# cast(ProtoType, my_dc)

print(type(ProtoType))
print(my_dc.__annotations__)
# print(dataclasses.fields(my_dc))
print(my_dc.data01)
print(my_dc.data02)
print(SoftBoiled.registered_classes)
