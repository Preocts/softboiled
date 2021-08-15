# SoftBoiled - Making flexible child dataclasses

### Why

I started using dataclasses to model API responses.  The self-constructing nature of the dataclass made the task very simple. In addition, having a model and not just a dict of the API response made the working code much cleaner.

This:
```json
{
  "id": 1,
  "name": "Some API Response",
  "details": {
    "id": 1,
    "name": "Some details"
  }
}
```

Was easy to create as a data model with:
```py
import dataclasses

@dataclasses.dataclass
class APIResponse:
    id: int
    name: str
    details: APIDetails

@dataclasses.dataclass
class APIDetails:
    id: int
    name: str

mapped_response = APIResponse(**json_response)
```

Of course this is vastly simplified. The API schema I started working with here were dozens of key/value pairs long with nested arrays and objects. But the pattern was there and it worked!  The `**` unpacking took care of the parameters and `dataclasses` did all the work.  I could even bring the model back to a dict form with `dataclasses.asdict(mapped_response)`.

The issues started when the API I was working with would add key/value pairs that were not in the official documentation.  Some objects gained key/value data depending on how they'd been used.  It wasn't important information but it broke the model with a single error:

`TypeError: __init__() got an unexpected keyword argument '[keyname]'`

The concept of the solution to this is straight-forward: Scrub your data before you create the dataclass instance.  `dataclasses` even has helper methods to facilitate this with `fields()`. Just remove what isn't expected *before* creating the model. Easy to apply at the top level `APIResponse` in my simple example. But how to apply that cleaning logic at the nested `APIDetails`?

---

### What

The immediate solution seemed to be not to use the built-in `__init__` of the dataclass. Instead, define my own `__init__` which accounted for extra values by ignoring them.  This quickly lead to bulky `__init__` defs in the dataclass definition with duplicated code in each new dataclass model.  There had to be a more programmatic solution.

That lead me to `SoftBoiled`. A parent class that, when inherited by a dataclass, gave me a simple method to create an instance.  The method would take the full dict response from the API, apply the cleaning process to the provided dict, and then use the built-in `__init__` of the dataclass to construct the model.

---

### Goal One [DONE]:

Create methods to be called from a parent class. This requires dataclasses to
be created using a `sbload()` class method.

### Goal Two [DONE]:

Add logic to handle a dataclass target that isn't a child of `SoftBoiled`. If that dataclass doesn't have a `sbload()` method then hand over the key/value parameters normally.

### Goal Three:

Pull `sbload()` out of the dataclass child and into `SoftBoiled`. This will leave the dataclass definition simple and clean.

### Stretch Goal:

Create a wrapper around the dataclass decorator, intercepting the parameters
before the `__init__` is called. This will allow a class to be initialized from
the `ClassName(...)` without a classmethod.

---

## Simple Start - single layer dataclass

With a single layer dataclass accomplish the following:
- Loads without error when missing fields
- Loads without error when fields match
- Loads without error when too many fields
- Alerts via logging if missing fields (inserted as `None`) are not `Optional` types

```py
@dataclasses.dataclass
class SimpleLayer(SafeLoader):
    data01: str
    data02: str
    data03: Optional[str]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> SimpleLayer:
        """create from dict"""
        return cls(**cls.cleandata(SimpleLayer, data))
```

---

## Nested Complexity - Dataclasses containing dataclasses

With a nested structure, which is far more likely with response models, there are a few more challenges to overcome.
- Accomplish every step of Simple Start
- Identify the type of the target key in the dataclass
  - Account for `Optional[]` and and `List[]` nestings of types
  - If the type is class
    - and the class is a dataclass
    - and the dataclass has a `sbload` method
    - call the `sbload` method (see note about arrays)
    - update the original value with the new instance
  - Else, keep original value

*Note on arrays*: It is common to have an array of objects in an API schema. The loading method must also take this into account and create an array of dataclasses when nessecary.

```py
@dataclasses.dataclass
class TopLayer(SoftBoiled):
    data01: str
    data02: NestedLayer
    data03: Optional[str]
    data04: Optional[List[NestedLayer]]

    @classmethod
    def sbload(cls, data: Dict[str, Any]) -> TopLayer:
        """create from dict"""
        return cls(**cls.cleandata(TopLayer, data))


@dataclasses.dataclass
class NestedLayer(SoftBoiled):
    data01: Optional[str]
    data02: bool

    @classmethod
    def sbload(cls, data: Dict[str, Any]) -> NestedLayer:
        """create from dict"""
        return cls(**cls.cleandata(NestedLayer, data))
```
