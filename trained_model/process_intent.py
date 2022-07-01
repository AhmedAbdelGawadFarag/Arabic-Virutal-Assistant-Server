import json
import os

import requests


def process(text, intent):
    if intent == 'call contact':
        print(os.getenv('ner_server_ip'))
        r = requests.post(os.getenv('ner_server_ip')+'/callContact', json={"text": text})
        print("response is")
        print(r.text)
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
