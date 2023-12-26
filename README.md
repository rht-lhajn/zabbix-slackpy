# slack.py

`slack.py` is one of zabbix alertscripts to send alert message for slack without any libraries.

## Usage

Put `src/slack.py` to `/usr/lib/zabbix/alertscripts/`.

### On media types

Set 2 parameters.

- `{ALERT.SENDTO}`
- `{ALERT.MESSAGE}`

### On actions

Set default message.

```json
{
    "date": "{DATE} / {TIME}",
    "host": "{HOST.NAME}",
    "name": "{TRIGGER.NAME}",
    "url": "{TRIGGER.URL}",
    "status": "{TRIGGER.STATUS}",
    "triage": "{TRIGGER.SEVERITY}",
    "item_name": "{ITEM.NAME}",
    "item_value": "{ITEM.VALUE}"
}
```

> `TRIGGER.URL` do not work well. Setting your zabbix dashboard page is recommended.

### On User Profile / Media

Set slack media and send to slack [incoming webhook URL](https://api.slack.com/incoming-webhooks).

## LICENSE

MIT
