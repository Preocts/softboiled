"""
The goal here is to create a nested dataclass that
filters its own parameters on init
"""
from __future__ import annotations

import dataclasses
import logging
from typing import Any
from typing import Dict
from typing import NamedTuple
from typing import Optional
from typing import Type


class SafeLoader:
    log = logging.getLogger("SafeLoader")

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

            field = fields[key]

            if (field_obj := globals().get(field.type)) is not None:  # type: ignore
                if dataclasses.is_dataclass(field_obj):

                    return_data.update({key: field_obj.from_dict(value)})
                    continue

            return_data.update({key: value})

        return return_data


@dataclasses.dataclass
class TopLayer(SafeLoader):
    data01: str
    data02: NestedLayer
    data03: Optional[str]
    data04: Optional[NamedTuple]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> TopLayer:
        """create from dict"""
        return cls(**cls.cleandata(TopLayer, data))


@dataclasses.dataclass
class NestedLayer(SafeLoader):
    data01: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> NestedLayer:
        """create from dict"""
        return cls(**cls.cleandata(NestedLayer, data))


class NotDC(NamedTuple):
    data01: str


print(dataclasses.fields(TopLayer))
