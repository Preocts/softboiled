"""
The goal here is to create a nested dataclass that
filters its own parameters on init
"""
import dataclasses
import logging
from typing import Any
from typing import Dict
from typing import Type


class SoftBoiled:
    log = logging.getLogger("SoftBoiled")

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

            field_type = fields[key].type
            # Possible hinting includes Optional[] and List[] so strip these out
            for search in ["Optional", "List", "[", "]"]:
                field_type = field_type.replace(search, "")

            if fobj := globals().get(field_type):  # type: ignore

                # Find the constructor: if a SoftBoil 'sbload' exists use that
                # else assume the __init__ can handle the info
                constr = fobj.sbload if getattr(fobj, "sbload", False) else fobj

                if isinstance(value, list):
                    values = [constr(inner) for inner in value]
                    return_data.update({key: values})
                else:
                    return_data.update({key: constr(value)})
                continue

            return_data.update({key: value})

        return return_data
