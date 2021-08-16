"""
The goal here is to create a nested dataclass that
filters its own parameters on init
"""
from __future__ import annotations

import dataclasses
import functools
import logging
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Type


class SoftBoiled:
    log = logging.getLogger("SoftBoiled")
    platter: Dict[str, Any] = {}

    def __init__(self, cls: Type[Any]) -> None:
        self.cls = cls

        SoftBoiled.platter.update({cls.__name__: cls})

        functools.update_wrapper(self, cls)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self.cls(*args, **SoftBoiled.cleandata(self.cls, kwargs))

    def __repr__(self) -> str:
        return repr(self.cls)

    @staticmethod
    def cleandata(obj: Type[Any], data: Dict[str, Any]) -> Dict[str, Any]:
        """Cleans data, removing keys that are not supported by object"""

        expected = [field.name for field in dataclasses.fields(obj)]

        cleandata = {key: value for key, value in data.items() if key in expected}

        nesteddata = SoftBoiled.__createnested(obj, cleandata)

        fulldata = SoftBoiled.__addmissing(obj, nesteddata)

        return fulldata

    @staticmethod
    def __addmissing(obj: Type[Any], data: Dict[str, Any]) -> Dict[str, Any]:
        """Adds missing key/values as None. Warns if not optional"""

        return_data: Dict[str, Any] = {}

        for field in dataclasses.fields(obj):
            new_value = data[field.name] if field.name in data else None
            return_data.update({field.name: new_value})

            if new_value is None and "Optional" not in field.type:
                SoftBoiled.log.warning(
                    "Type Warning: required key missing, now None '%s'", field.name
                )

        return return_data

    @staticmethod
    def __createnested(obj: Type[Any], data: Dict[str, Any]) -> Dict[str, Any]:
        """Create nested dataclass objects with sbload calls"""

        return_data: Dict[str, Any] = {}
        fields = {field.name: field for field in dataclasses.fields(obj)}

        for key, value in data.items():

            field_type = str(fields[key].type)
            # Possible hinting includes Optional[] and List[] so strip these out
            for search in ["Optional", "List", "[", "]"]:
                field_type = field_type.replace(search, "")

            if field_type in SoftBoiled.platter:
                constr = SoftBoiled.platter[field_type]

                if isinstance(value, list):
                    values = [constr(**inner) for inner in value]
                    return_data.update({key: values})
                else:
                    return_data.update({key: constr(**value)})
                continue

            return_data.update({key: value})

        return return_data


INNER_NEST_SMALL: Dict[str, Any] = {"data01": "Hi"}
INNER_NEST: Dict[str, Any] = {
    "data01": "Hi",
    "data02": True,
    "data03": {"data01": "Norm"},
}
INNER_NEST_LARGE: Dict[str, Any] = {
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


@SoftBoiled
@dataclasses.dataclass
class TopLayer:
    data01: str
    data02: NestedLayer
    data03: Optional[str]
    data04: Optional[List[NestedLayer]]


@SoftBoiled
@dataclasses.dataclass
class NestedLayer:
    data01: Optional[str]
    data02: bool
    data03: NestedNorm


@dataclasses.dataclass
class NestedNorm:
    data01: str = ""


if __name__ == "__main__":
    result = TopLayer(**JUST_RIGHT)
    print("&" * 79)
    print(result)
