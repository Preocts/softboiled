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
