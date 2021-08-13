"""
The goal here is to create a single deep dataclass that
filters its own parameters on init
"""
from __future__ import annotations

import dataclasses
import logging
from typing import Any
from typing import Dict
from typing import Optional
from typing import Type


class SafeLoader:
    log = logging.getLogger("SafeLoader")

    @staticmethod
    def cleandata(obj: Type, data: Dict[str, Any]) -> Dict[str, Any]:
        """Cleans data, removing keys that are not supported by object"""

        fulldata = SafeLoader.__addmissing(obj, data)
        expected = [field.name for field in dataclasses.fields(obj)]

        return {key: value for key, value in fulldata.items() if key in expected}

    @staticmethod
    def __addmissing(obj: Type, data: Dict[str, Any]) -> Dict[str, Any]:
        """Adds missing key/values as None. Warns if not optional"""

        return_data: Dict[str, Any] = {}

        for field in dataclasses.fields(obj):

            if field.name not in data:
                return_data.update({field.name: None})

                if "Optional" not in field.type:
                    SafeLoader.log.warning(
                        "Type Warning: required key missing, now None '%s'", field.name
                    )

            else:

                return_data.update({field.name: data[field.name]})

        return return_data


@dataclasses.dataclass
class SimpleLayer(SafeLoader):
    data01: str
    data02: str
    data03: Optional[str]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> SimpleLayer:
        """create from dict"""
        return cls(**cls.cleandata(SimpleLayer, data))
