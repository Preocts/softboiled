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

### Step One:

Create methods to be called from a parent class. This requires dataclasses to
be created using a `from_dict()` class method.

### Step Two:

Create a wrapper around the dataclass decorator, intercepting the parameters
before the `__init__` is called. This will allow a class to be initialized from
the `ClassName(...)` without a classmethod.
