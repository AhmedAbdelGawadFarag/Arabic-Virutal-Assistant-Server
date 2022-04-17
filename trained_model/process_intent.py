import json

import requests
import config as config


def process(text, intent):
    if intent == 'call contact':
        r = requests.post(config.ip_address, json={"data": text})
        print("response is")
        r = json.loads(r.text)
        print(r['data'])
        return r['data']
    if intent == 'search':
        arr = text.split(" ")
        res = ""
        for i in range(2, len(arr)):
            res += arr[i] + " "
        print(res)
        return res
