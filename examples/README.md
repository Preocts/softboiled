# Examples

## example.py

Very simple example as seen on the root `README.md`

---

## [pduser.py](pduser.py)

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


Example input to handle:

*taken from [https://developer.pagerduty.com/api-reference/reference/REST/openapiv3.json/paths/~1users/get](https://developer.pagerduty.com/api-reference/reference/REST/openapiv3.json/paths/~1users/get)*
```json
{
    "name": "Alan B. Shepard, Jr.",
    "email": "alan.shepard@nasa.example",
    "time_zone": "America/Los_Angeles",
    "color": "blue-violet",
    "avatar_url": "https://secure.gravatar.com/avatar/e58b7fdfb50566fd0334b360a05b729c.png?d=mm&r=PG",
    "billed": true,
    "role": "limited_user",
    "description": null,
    "invitation_sent": true,
    "job_title": null,
    "teams": [
        {
            "id": "PQZPQGI",
            "name": "North American Space Agency (NASA)",
            "description": null,
            "type": "team",
            "summary": "North American Space Agency (NASA)",
            "self": "https://api.pagerduty.com/teams/PQZPQGI",
            "html_url": "https://pdt-apidocs.pagerduty.com/teams/PQZPQGI",
            "default_role": "manager",
            "parent": null
        }
    ],
    "contact_methods": [
        {
            "id": "PSMLP14",
            "type": "email_contact_method_reference",
            "summary": "Default",
            "self": "https://api.pagerduty.com/users/PLOASXQ/contact_methods/PSMLP14",
            "html_url": null
        },
        {
            "id": "P3W47MP",
            "type": "phone_contact_method_reference",
            "summary": "Work",
            "self": "https://api.pagerduty.com/users/PLOASXQ/contact_methods/P3W47MP",
            "html_url": null
        },
        {
            "id": "PBXT65T",
            "type": "sms_contact_method_reference",
            "summary": "Mobile",
            "self": "https://api.pagerduty.com/users/PLOASXQ/contact_methods/PBXT65T",
            "html_url": null
        }
    ],
    "notification_rules": [
        {
            "id": "PJGOM3Q",
            "type": "assignment_notification_rule_reference",
            "summary": "0 minutes: channel PSMLP14",
            "self": "https://api.pagerduty.com/users/PLOASXQ/notification_rules/PJGOM3Q",
            "html_url": null
        },
        {
            "id": "P0K2LG6",
            "type": "assignment_notification_rule_reference",
            "summary": "0 minutes: channel PSMLP14",
            "self": "https://api.pagerduty.com/users/PLOASXQ/notification_rules/P0K2LG6",
            "html_url": null
        },
        {
            "id": "PKWQ7KR",
            "type": "assignment_notification_rule_reference",
            "summary": "0 minutes: channel P3W47MP",
            "self": "https://api.pagerduty.com/users/PLOASXQ/notification_rules/PKWQ7KR",
            "html_url": null
        },
        {
            "id": "PW2553L",
            "type": "assignment_notification_rule_reference",
            "summary": "0 minutes: channel PBXT65T",
            "self": "https://api.pagerduty.com/users/PLOASXQ/notification_rules/PW2553L",
            "html_url": null
        }
    ],
    "coordinated_incidents": [],
    "id": "PLOASXQ",
    "type": "user",
    "summary": "Alan B. Shepard, Jr.",
    "self": "https://api.pagerduty.com/users/PLOASXQ",
    "html_url": "https://pdt-apidocs.pagerduty.com/users/PLOASXQ"
}
```

### Code to parse data into dataclass:

*Dataclasses defined already. This just showcases creating an instance of the dataclass.*

```py
user = PagerdutyUser(**user_json)
```
