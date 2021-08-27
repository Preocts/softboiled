[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/Preocts/softboiled/main.svg)](https://results.pre-commit.ci/latest/github/Preocts/softboiled/main)
[![Python package](https://github.com/Preocts/softboiled/actions/workflows/python-tests.yml/badge.svg?branch=main)](https://github.com/Preocts/softboiled/actions/workflows/python-tests.yml)

# SoftBoiled - Making overly flexible dataclasses

A dataclass decorator that cleans the parameters on instance creation to account for missing or extra keyword arguments. Allows for faster, if messier, modeling of API responses that are lacking in firm schema.

## Requirements
- Python >= 3.8

## Installation

Installation
**Note**: Replace `1.x.x` with the desired version number or `main` for latest (unstable) version

Install via pip with pypi:
```
pip install softboiled==1.x.x
```

Install via pip with GitHub:
```
# Linux/MacOS
python3 -m pip install git+https://github.com/preocts/softboiled@v1.x.x

# Windows
py -m pip install git+https://github.com/preocts/softboiled@v1.x.x
```

---

## Known Limitations

- All dataclass objects within a SoftBoiled dataclass must also be SoftBoiled

---

## [Example Usage](example/example.py)

The documentation says to expect the following API response:
```py
EXAMPLE01 = {
  "id": 1,
  "name": "Example Response v1",
  "details": {
    "color": "blue",
    "number": 42,
    "true": False
  },
  "more": False
}
```

However, the API response is actually:
```py
EXAMPLE02 = {
  "id": 1,
  "name": "Example Response v1",
  "status": "depreciated",
  "details": {
    "color": "blue",
    "number": 42,
    "size": "medium"
  },
  "more": False
}
```

The additional field `status` and missing field `details.true` are not consistant in *all* of the API responses and cannot be safely mapped.  Time for a `Softboiled` dataclass:

```py
from __future__ import annotations

import dataclasses

from softboiled import SoftBoiled


@SoftBoiled
@dataclasses.dataclass
class ExampleAPIModel:
    id: int
    name: str
    details: ExampleAPISubModel
    more: bool


@SoftBoiled
@dataclasses.dataclass
class ExampleAPISubModel:
    color: str
    number: int
    true: bool
    size: str


EXAMPLE01 = {
    "id": 1,
    "name": "Example Response v1",
    "details": {"color": "blue", "number": 42, "true": False},
    "more": False,
}

EXAMPLE02 = {
    "id": 1,
    "name": "Example Response v1",
    "status": "depreciated",
    "details": {"color": "blue", "number": 42, "size": "medium"},
    "more": False,
}

valid_model01 = ExampleAPIModel(**EXAMPLE01)
valid_model02 = ExampleAPIModel(**EXAMPLE02)

print(valid_model01)
print(valid_model02)
```

Output:
```
Type Warning: required key missing, now None 'size'
Type Warning: required key missing, now None 'true'
ExampleAPIModel(id=1, name='Example Response v1', details=ExampleAPISubModel(color='blue', number=42, true=False, size=None), more=False)
ExampleAPIModel(id=1, name='Example Response v1', details=ExampleAPISubModel(color='blue', number=42, true=None, size='medium'), more=False)
```

Both models will be created without errors. The extra field `status` will be dropped and the missing field `details.true` will be created with a `NoneType` value for `valid_model02`.

The `Type Warning` is indicating that a value was missing and replaced with `None`.  Type-hinting the key as optional (`size: Optional[str]`) eliminates the warning.  Giving the attribute a default assignment in the dataclass will also remove the warning as the default will be used.


---
---

### Why:

Because data isn't perfect.

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

The immediate solution seemed to be not to use the built-in `__init__` of the dataclass. Instead, define my own `__init__` which accounted for extra values by ignoring them.  This quickly lead to bulky `__init__` defs in the dataclass definition with duplicated code in each new dataclass model.  There had to be a more programmatic solution.

That lead me to `SoftBoiled`. A decorater for dataclasses. Once wrapped, the dataclass has the incoming key/value data scrubbed. Extra pairs are removed to avoid the `TypeError`. Missing pairs are added with a value of `None`, if they don't have a default assignment. Nested Dataclasses are treated with the same care.

This leaves creating the model as simple as defining the structure of the dataclass and then unpacking an API's JSON response into it.

---
---

## Local developer installation

It is **highly** recommended to use a [virtual environment](https://docs.python.org/3/library/venv.html) (`venv`) for installation. Leveraging a `venv` will ensure the installed dependency files will not impact other python projects.

Clone this repo and enter root directory of repo:
```bash
$ git clone https://github.com/preocts/softboiled
$ cd softboiled
```

Create and activate `venv`:
```bash
# Linux/MacOS
python3 -m venv venv
. venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate.bat
# or
py -m venv venv
venv\Scripts\activate.bat
```

Your command prompt should now have a `(venv)` prefix on it.

Install editable library and development requirements:
```bash
# Linux/MacOS
pip install -r requirements-dev.txt
pip install --editable .

# Windows
python -m pip install -r requirements-dev.txt
python -m pip install --editable .
# or
py -m pip install -r requirements-dev.txt
py -m pip install --editable .
```

Install pre-commit hooks to local repo:
```bash
pre-commit install
pre-commit autoupdate
```

Run tests
```bash
tox
```

To exit the `venv`:
```bash
deactivate
```

---

### Makefile

This repo has a Makefile with some quality of life scripts if your system supports `make`.

- `install` : Clean all artifacts, update pip, install requirements with no updates
- `update` : Clean all artifacts, update pip, update requirements, install everything
- `clean-pyc` : Deletes python/mypy artifacts
- `clean-tests` : Deletes tox, coverage, and pytest artifacts
- `build-dist` : Build source distribution and wheel distribution
