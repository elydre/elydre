import json
import time

import requests
from pyzabbix.api import ZabbixAPI

def send_discord_embed(webhook_url, color, host, to, msg, event_id):
    payload = {
        "embeds": [
            {
            "title": "ZABBIX WARNING",
            "url": "http://zabbix.pf/zabbix/",
            "description": "un problème est survenu dans l'infra :poop:",
            "color": int(color[1:], 16),
            "fields": [
                {
                "name": "Serveur",
                "value": host,
                "inline": True
                },
                {
                "name": "Depuis",
                "value": to,
                "inline": True
                },
                {
                "name": "Description",
                "value": msg,
                },
            ],
            "footer": {
                "text": f"elydre - eventid: {event_id}",
                "icon_url": "https://avatars.githubusercontent.com/u/74263128?v=4"
            }
            }
        ]
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(webhook_url, data=json.dumps(payload), headers=headers)

colors = [
    "#b4b6c8",
    "#9097ff",
    "#ffdc2f",
    "#ffa953",
    "#ff5e3a",
    "#da0019",]

# config the 2 next lines
webhook_url = ""
zapi = ZabbixAPI(url='', user='', password='')

sends = []

while True:
    print("bcl")
    ev = zapi.event.get(selectHosts='extend')
    pb = zapi.problem.get(selectHosts='extend')

    for e in ev:
        if [p for p in pb if p['clock'] == e['clock']] and int(e['eventid']) not in sends:
            to = time.strftime('%H:%M:%S', time.localtime(int(e['clock'])))
            host = e['hosts'][0]['host']
            color = colors[int(e['severity'])]
            msg = e['name']
            eventid = int(e['eventid'])
            send_discord_embed(webhook_url, color, host, to, msg, eventid)
            sends.append(eventid)
            time.sleep(5)
    
    time.sleep(60)