"""
Example use of SoftBoiled

User story:

As an engineer I need a data structure that represents a
single user in PagerDuty, so that we can leverage the
information in downstream automation.

Required data points:
- User Name
- PagerDuty ID
- Base permission level
- User's Teams
    - User's team id
    - User's team name
    - Team default role
"""
from __future__ import annotations

import dataclasses
import http.client
import json
from typing import Any
from typing import Dict
from typing import List

from softboiled import SoftBoiled


# Define data models. Not importing __future__ here so inner
# data models need to be defined before outter
@SoftBoiled
@dataclasses.dataclass
class PagerdutyTeam:
    """Create the inner-model for acceptance criteria"""

    id: str
    name: str
    default_role: str


@SoftBoiled
@dataclasses.dataclass
class PagerdutyUser:
    """
    Create a model of the acceptance criteria

    No need to worry about the entire structure, just what is needed
    """

    name: str
    id: str
    role: str
    teams: List[PagerdutyTeam]


def pagerduty_get_object(route: str) -> Dict[str, Any]:
    """
    Pulls from PagerDuty's public testing API

    The token here is not a secret.
    https://developer.pagerduty.com/api-reference/
    """

    conn = http.client.HTTPSConnection("api.pagerduty.com")

    headers = {
        "accept": "application/vnd.pagerduty+json;version=2",
        "content-type": "application/json",
        "authorization": "Token token=y_NbAkKc66ryYTWUXYEu",
    }

    conn.request("GET", route, headers=headers)

    res = conn.getresponse()
    data = res.read()

    return json.loads(data.decode("utf-8"))


def main() -> int:
    """
    Run the query and print the output

    All runs have more data being unpacked into the dataclass
    that what is defined for the dataclass

    First route:
        Show that we can pull incomplete data and not crash

    Second route:
        Show that we can pull complete data
    """
    route_strings = [
        "/users?limit=2",
        "/users?limit=2&include[]=teams",
    ]

    for route in route_strings:
        result = pagerduty_get_object(route)

        # Convert JSON loaded return to dataclass with **dict unpacking
        users = [PagerdutyUser(**user) for user in result["users"]]

        # Print results out
        print_results(users)

    return 0


def print_results(users: List[PagerdutyUser]) -> None:
    """Print the results"""
    print("\n" + "*" * 50 + "\n")

    for user in users:
        print(f"User ID: {user.id}")
        print(f"User name: {user.name}")
        print(f"User role: {user.role}")
        print(f"# of Teams: {len(user.teams)}")
        for idx, team in enumerate(user.teams):
            print(f"\tTeam {idx + 1} id: {team.id}")
            print(f"\tTeam {idx + 1} name: {team.name}")
            print(f"\tTeam {idx + 1} default role: {team.default_role}")


if __name__ == "__main__":
    raise SystemExit(main())
