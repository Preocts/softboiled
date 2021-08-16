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
                    values = [SoftBoiled.cleandata(constr, inner) for inner in value]
                    values = [constr(**inner) for inner in values]
                    return_data.update({key: values})
                else:
                    return_data.update(
                        {key: constr(**SoftBoiled.cleandata(constr, value))}
                    )
                continue

            return_data.update({key: value})

        return return_data
