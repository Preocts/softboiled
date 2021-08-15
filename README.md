# Dataclasses

Playing around with making simple, but flexible dataclasses for modeling API
responses.

### Challenge

While many REST APIs out there are well documented and easily modeled, there
are a few that break this norm. Their structure is fey and fickle with
unexpected key/value pairs appearing along side unexpected null values.

`dataclasses.dataclass` seems to be the best solution for quickly prototyping
out the model. The only exception is when *more* key/values exist than
expected.

### Proposed Solution

Create a parent class that contains utility methods which strip incoming data
down. Extra keys will not be passed to the `__init__` of the dataclass.

### Goal One:

Create methods to be called from a parent class. This requires dataclasses to
be created using a `sbload()` class method.

### Goal Two:

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
