import requests
import time
import json

QUEUEHOST  = "192.168.93.174"
QUEUEPORT  = 18888
STARTPATH   = "/start"

def GetURLPath(HOST,PORT,PATH):
    return "http://" + str(HOST) + ":" + str(PORT) + PATH
cls = input("是否启动Y/n:")

if cls == "Y" or cls == "y":
    r = requests.post(GetURLPath(QUEUEHOST,QUEUEPORT,STARTPATH),data=json.dumps({"token":"243e21045c0c2912f5315907c8fc0775"}))
    print(r.text)

while True:
    time.sleep(2)
    r = requests.post(GetURLPath(QUEUEHOST,QUEUEPORT,'/status'),data=json.dumps({"token":"243e21045c0c2912f5315907c8fc0775"}))
    result = json.loads(r.text)
    error = result["error"]
    if error == '1':
        now = result["now"]
        All = result["All"]
        print("进度{}/{}".format(now,All),end='\r')
        if now >= All:
            print("终于跑完啦！！")
            break

