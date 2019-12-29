from lib.data import QUEUEHOST,QUEUEPORT,TASKPATH,SCRIPT,TASK,VERSION,BUMBLEID,TOKEN,RESULT
from lib.loader import load_string_to_module
from lib.threads import WorkeBee
import requests
import base64
import time
import json
import re



def banner():
    msg = '''
######                                     ######  ####### ####### 
#     # #    # #    # #####  #      ###### #     # #       #       
#     # #    # ##  ## #    # #      #      #     # #       #       
######  #    # # ## # #####  #      #####  ######  #####   #####   
#     # #    # #    # #    # #      #      #     # #       #       
#     # #    # #    # #    # #      #      #     # #       #       
######   ####  #    # #####  ###### ###### ######  ####### ####### {}
    '''.format(VERSION)
    print(msg)


proxies = {
  "http": "http://192.168.93.1:8080",
  "https": "http://192.168.93.1:8080",
}

def GetURLContent(URL):
    r = requests.get(URL)
    return r.content

def GetURLPath(HOST,PORT,PATH):
    return "http://" + str(HOST) + ":" + str(PORT) + PATH


def GetTaskAndScript():
    '''获取任务及攻击脚本'''
    global SCRIPT,TASK
    result = requests.post(GetURLPath(QUEUEHOST,QUEUEPORT,TASKPATH),data=json.dumps({'bumbleID':BUMBLEID}),proxies=proxies).content
    result = json.loads(result)
    if result['error'] == "0":
        print('获取任务列表：暂无任务',end='\r')
        return False
    SCRIPT = base64.b64decode(result["script"]) # 记得修改
    TASK = result["list"]
    print("获取任务列表：{0}....".format(TASK[:20]))
    return True

def register():
    global BUMBLEID
    """初始化函数，WorkeBEE向QueueBEE注册"""
    print("正在向QueueBee注册WokerBee")
    token=json.dumps({"token":TOKEN})
    r = requests.post(GetURLPath(QUEUEHOST,QUEUEPORT,"/register"),data=token)
    content = json.loads(r.text)
    ERROR = content["error"]
    if ERROR == "1":
        BUMBLEID = content["bumbleID"]
        print("获取BUMBLEID为{}".format(BUMBLEID))
    else:
        print("token错误")
        exit()

def submission():
    print("\n正在提交任务结果...\n")
    result = requests.post(GetURLPath(QUEUEHOST,QUEUEPORT,"/submission"),data=json.dumps({'bumbleID':BUMBLEID,'result':RESULT})).content
    result = json.loads(result)
    if result['error'] == "0":
        print("提交任务结果失败")
    else:
        print("提交任务结果成功")


def main():
    global SCRIPT,TASK,RESULT
    banner()    #显示banner信息
    register()  #向Queue注册
    while True:
        if GetTaskAndScript():                      #获取脚本及任务
            SCRIPT = load_string_to_module(SCRIPT)  #加载脚本
            worker = WorkeBee(SCRIPT,TASK)          #WorkeBee初始化
            worker.run()                            #WorkeBee运行
            RESULT = worker.get_result()            #获取结果
            # print(RESULT)
            submission()
            
        time.sleep(1)

if __name__ == "__main__":
    main()
