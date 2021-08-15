"""
The goal here is to create a nested dataclass that
filters its own parameters on init
"""
from __future__ import annotations

import dataclasses
import logging
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Type


class SafeLoader:
    log = logging.getLogger("SafeLoader")

    SUPPORTED_TYPES = [int, float, str, bool, list, dict, None]

    @staticmethod
    def cleandata(obj: Type[Any], data: Dict[str, Any]) -> Dict[str, Any]:
        """Cleans data, removing keys that are not supported by object"""

        expected = [field.name for field in dataclasses.fields(obj)]

        cleandata = {key: value for key, value in data.items() if key in expected}

        nesteddata = SafeLoader.__createnested(obj, cleandata)

        fulldata = SafeLoader.__addmissing(obj, nesteddata)

        return fulldata

    @staticmethod
    def __addmissing(obj: Type[Any], data: Dict[str, Any]) -> Dict[str, Any]:
        """Adds missing key/values as None. Warns if not optional"""

        return_data: Dict[str, Any] = {}

        for field in dataclasses.fields(obj):
            new_value = data[field.name] if field.name in data else None
            return_data.update({field.name: new_value})

            if new_value is None and "Optional" not in field.type:
                SafeLoader.log.warning(
                    "Type Warning: required key missing, now None '%s'", field.name
                )

        return return_data

    @staticmethod
    def __createnested(obj: Type[Any], data: Dict[str, Any]) -> Dict[str, Any]:
        """Create nested dataclass objects with from_dict calls"""

        return_data: Dict[str, Any] = {}
        fields = {field.name: field for field in dataclasses.fields(obj)}

        for key, value in data.items():

            field_type = fields[key].type

            # Possible nesting includes Optional[] and List[]
            # Strip these down
            if field_type.startswith("Optional["):
                field_type = field_type.lstrip("Optional[").rstrip("]")
            if field_type.startswith("List["):
                field_type = field_type.lstrip("List[").rstrip("]")

            if (field_obj := globals().get(field_type)) is not None:  # type: ignore

                if isinstance(value, list):
                    values = [field_obj.from_dict(inner) for inner in value]
                    return_data.update({key: values})
                else:
                    return_data.update({key: field_obj.from_dict(value)})
                continue

            return_data.update({key: value})

        return return_data


@dataclasses.dataclass
class TopLayer(SafeLoader):
    data01: str
    data02: NestedLayer
    data03: Optional[str]
    data04: Optional[List[NestedLayer]]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> TopLayer:
        """create from dict"""
        return cls(**cls.cleandata(TopLayer, data))


@dataclasses.dataclass
class NestedLayer(SafeLoader):
    data01: Optional[str]
    data02: bool

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> NestedLayer:
        """create from dict"""
        return cls(**cls.cleandata(NestedLayer, data))


if __name__ == "__main__":

    INNER_NEST_SMALL = {"data01": "Hi"}
    INNER_NEST = {"data01": "Hi", "data02": True}
    INNER_NEST_LARGE = {"data01": "Hi", "data02": True, "data03": "wut"}

    INNER_LIST = [INNER_NEST, INNER_NEST, INNER_NEST]

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

    print("++ Exact match to expected input:")
    print(f"\n{TopLayer.from_dict(JUST_RIGHT)}\n")

    print("++ Too much data provided at base and inner layers:")
    print(f"\n{TopLayer.from_dict(TOO_MUCH)}\n")

    print("++ Not enough data provided at base or inner layers:")
    print(f"\n{TopLayer.from_dict(TOO_SMALL)}\n")
