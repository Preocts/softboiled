"""
Dataclass decorator that cleans creation parameters

A dataclass decorator that cleans the parameters on instance creation
to account for missing or extra keyword arguments. Allows for faster,
if messier, modeling of API responses that are lacking in firm schema.

Author: Preocts, discord: Preocts#8196
"""
import dataclasses
import functools
import logging
import re
from dataclasses import is_dataclass
from dataclasses import MISSING
from typing import Any
from typing import Dict
from typing import Type


class SoftBoiled:
    """Dataclass decorator that cleans creation parameters"""

    log = logging.getLogger("SoftBoiled")
    platter: Dict[str, Any] = {}

    def __init__(self, cls: Type[Any]) -> None:
        """Wraps a dataclasses.dataclass and registers class name internally"""
        if not is_dataclass(cls):
            raise ValueError("Expected dataclass obejct, got %s", type(cls))

        self.cls = cls

        SoftBoiled.platter.update({cls.__name__: cls})

        functools.update_wrapper(self, cls)

    def __call__(self__, *args: Any, **kwargs: Any) -> Any:
        """Handles cleaning kwargs before creating dataclass"""
        return self__.cls(*args, **SoftBoiled.cleandata(self__.cls, kwargs))

    def __repr__(self) -> str:
        """Identify has the decorated class"""
        return repr(self.cls)

    @staticmethod
    def cleandata(obj: Type[Any], data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cleans data, removing keys that are not supported by object

        Args:
            obj: The class object that has been decorated
            data: kwargs of the creation call for the decorated class
        """

        expected = [field.name for field in dataclasses.fields(obj)]

        cleandata = {key: value for key, value in data.items() if key in expected}

        nesteddata = SoftBoiled.__createnested(obj, cleandata)

        fulldata = SoftBoiled.__addmissing(obj, nesteddata)

        return fulldata

    @staticmethod
    def __addmissing(obj: Type[Any], data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Adds missing key/values as None. Warning to console if not optional

        Args:
            obj: The class object that has been decorated
            data: kwargs of the creation call for the decorated class
        """
        return_data: Dict[str, Any] = {}

        for field in dataclasses.fields(obj):

            if field.name in data:
                new_value = data[field.name]
            else:
                new_value = field.default if field.default is not MISSING else None

            return_data.update({field.name: new_value})

            if new_value is None and "Optional" not in str(field.type):
                SoftBoiled.log.warning(
                    "Type Warning: required key missing, now None '%s'", field.name
                )

        return return_data

    @staticmethod
    def __createnested(obj: Type[Any], data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create nested dataclass objects with sbload calls

        Args:
            obj: The class object that has been decorated
            data: kwargs of the creation call for the decorated class
        """

        return_data: Dict[str, Any] = {}
        fields = {field.name: field for field in dataclasses.fields(obj)}

        for key, value in data.items():

            finaldata: Any = value

            for softboiled in SoftBoiled.platter:
                # Find the SoftBoiled class name in the type string
                match = re.findall(rf"\b{softboiled}\b", str(fields[key].type))

                if match:

                    constr = SoftBoiled.platter[match[0]]

                    if isinstance(value, list):
                        cleandata = [SoftBoiled.cleandata(constr, val) for val in value]
                        finaldata = [constr(**inner) for inner in cleandata]
                    else:
                        finaldata = constr(**SoftBoiled.cleandata(constr, value))

            return_data.update({key: finaldata})

        return return_data
