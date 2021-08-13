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
be created using a `from_dict()` class method.

### Goal Two:

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

### Results - PASSED
