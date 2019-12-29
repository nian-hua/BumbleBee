import requests
import re

def BumbleBeeWorker(HOST):
    try:
        r = requests.get(HOST)
        r.encoding = 'utf-8'
        context = re.findall(r'<title>(.*?)</title>', r.text)
        if context != []:
            return context[0]
    except:
        return 0
