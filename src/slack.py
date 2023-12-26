#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Forked from: https://github.com/h-otter/zabbix-slackpy
# Repository: https://github.com/Red-Hat-Information-Security/zabbix-slackpy

import configparser
import requests
from json import loads
from sys import argv

request_timeout = 1800


def get_triager(file: str) -> str:
    """
    Return current triager Slack ID
    """
    config = configparser.ConfigParser()
    config.read(file)

    return config['triage']['notify']


def send_trigger(notify, message, slack_hook):
    """
    On zabbix, set actions to architect message like this
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
    """
    title = f"{message['status']}: {message['name']}"

    if message["status"] == "PROBLEM":
        if message["triage"] == "Disaster":
            color = "#e45959"
        elif message["triage"] == "High":
            color = "#e97659"
        elif message["triage"] == "Average":
            color = "#ffa059"
        elif message["triage"] == "Warning":
            color = "#ffc859"
        elif message["triage"] == "Information":
            color = "#7499ff"
        else:
            color = "#97aab3"

        payload = {
            "attachments": [
                {
                    "fallback": f"{message['date']} - {title}.",
                    "color": color,
                    "author_name": "Zabbix",
                    "author_icon": "https://assets.zabbix.com/img/favicon.ico",
                    "title": title,
                    "title_link": message["url"],
                    "fields": [
                        {
                            "title": "Host",
                            "value": message["host"],
                            "short": False
                        },
                        {
                            "title": "Data",
                            "value": message["date"],
                            "short": False
                        },
                        {
                            "title": "Detail",
                            "value": f"{message['item_name']}: {message['item_value']}.",
                            "short": False
                        },
                        {
                            "title": "Triager",
                            "value": f'<{notify}>',
                            "short": False
                        },
                    ],
                }
            ]
        }

    elif message["status"] == 'OK':
        if message["triage"] in ["Disaster", "High", "Average", "Warning"]:
            color = "good"
        else:
            return

        payload = {
            "attachments": [
                {
                    "fallback": f"{message['date']} - {title}.",
                    "color": color,
                    "author_name": "Zabbix",
                    "author_icon": "https://assets.zabbix.com/img/favicon.ico",
                    "title": title,
                    "title_link": message["url"],
                    "text": f"Host: {message['host']}",
                }
            ]
        }

    else:
        raise Exception(f"Unsupported alert status: {message['status']}.")

    headers = {'Content-type':'application/json'}

    response = requests.post(
        slack_hook, headers=headers, json=payload, timeout=request_timeout
    )


if __name__ == "__main__":
    """
    On zabbix, set media type for slack like these
    - parameters
        - {ALERT.SENDTO} -> set Slack hook URL on user configuration
        - {ALERT.MESSAGE}
    """
    argvs = argv
    if len(argvs) < 3:
        print("\nToo few arguments -- requires: (slack_hook message). Example console run:\n")
        print("""python slack.py https://hooks.slack.com/services/SLACKHOSTID '{ "date": "2020-01-01 / 00:00:01", "host": "times.square", "name": "NewYears", "url": "https://www.timeanddate.com/countdown/newyear", "status": "PROBLEM", "triage": "Warning", "item_name": "Countdown Clock", "item_value": "Almost there" }' """ + "\n")
    else:
        triager = get_triager('/usr/lib/zabbix/alertscripts/triage.ini')
        loaded = loads(argvs[2])
        send_trigger(triager, loaded, argvs[1])
