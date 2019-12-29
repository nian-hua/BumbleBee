from flask import Flask
from flask import request
import hashlib
import random
import base64
import time
import json
import re
app = Flask(__name__)

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

TOKEN = "243e21045c0c2912f5315907c8fc0775"
BUMBLEIDLIST = {}
COMPLETELIST = {}
MISSION = False
SCRIPT = ''
TASKLIST = []
RESULT = []
COUNT = 0

@app.route('/')
def hello_world():
    return 'BumbleBee'

@app.route('/register',methods=['POST'])
def register():
    token = request.get_json(force=True)
    token = token['token']
    if token == TOKEN:
        bumbleID = random_md5()
        BUMBLEIDLIST[bumbleID] = 0
        COMPLETELIST[bumbleID] = True
        result = {"error":"1","bumbleID":bumbleID}
    else:
        result = {"error":"0"}
    print(BUMBLEIDLIST)
    result = json.dumps(result)
    return result

@app.route('/task',methods=['POST'])
def task():
    global COUNT,MISSION
    bumbleID = request.get_json(force=True)
    bumbleID = bumbleID['bumbleID']
    # print(bumbleID,MISSION,COMPLETELIST[bumbleID])
    if MISSION and COMPLETELIST[bumbleID]:
        time.sleep(1)
        print(str(BUMBLEIDLIST[bumbleID])[:20])
        result = {"error":"1","script":SCRIPT,"list":BUMBLEIDLIST[bumbleID]}
        COMPLETELIST[bumbleID] = False
        COUNT += 1
    else:
        result = {"error":"0"}
    # print(result)
    if COUNT >= len(BUMBLEIDLIST):
         MISSION = False
    result = json.dumps(result)
    return result

@app.route('/status',methods=['POST'])
def status():
    global RESULT,TASKLIST,TOKEN
    token = request.get_json(force=True)
    token = token['token']
    if token == TOKEN:
        result = {"error":"1","now":len(RESULT),"All":len(TASKLIST)}
    else:
        result = {"error":"0"}
    result = json.dumps(result)
    return result


@app.route('/start',methods=['POST'])
def start():
    global MISSION,COUNT,RESULT
    token = request.get_json(force=True)
    token = token['token']
    if len(BUMBLEIDLIST) < 1:
        return '暂时无工作节点接入'
    if token == TOKEN:
        COUNT = 0
        RESULT = []
        load()
        TaskCount = len(TASKLIST)
        UserCount = len(BUMBLEIDLIST)
        Average = TaskCount//UserCount
        print(TaskCount,UserCount,Average)
        i = 0
        for key in list(BUMBLEIDLIST.keys()):
            if i != len(BUMBLEIDLIST) - 1:
                BUMBLEIDLIST[key] = TASKLIST[i*Average:(i+1)*Average]
            else:
                BUMBLEIDLIST[key] = TASKLIST[i*Average:]
            i += 1
        # print(BUMBLEIDLIST)
        for key in list(BUMBLEIDLIST.keys()):
            print(len(BUMBLEIDLIST[key] ))
        MISSION = True
        result = {"error":"1"}
    else:
        result = {"error":"0"}
    result = json.dumps(result)
    return result

@app.route('/submission',methods=['POST'])
def submission():
    global MISSION,COMPLETELIST,BUMBLEIDLIST,RESULT
    submission = request.get_json(force=True)
    bumbleID = submission['bumbleID']
    result = submission['result']
    print(result)
    BUMBLEIDLIST[bumbleID] = 0
    COMPLETELIST[bumbleID] = True
    RESULT += result
    if len(RESULT) == len(TASKLIST):
        fw = open("result.txt","w")
        for i in RESULT:
            fw.writelines(str(i)+'\n')
        fw.close()
        MISSION = False
    return json.dumps({"error":"1"})

def load():
    global SCRIPT,TASKLIST
    fr = open('script.py')
    SCRIPT = fr.read()
    fr.close()
    if isinstance(SCRIPT, str):
        SCRIPT = SCRIPT.encode(encoding='UTF-8')
    SCRIPT = base64.b64encode(SCRIPT).decode('ascii')
    
    with open('task.txt', 'r') as f:
        for line in f:
            TASKLIST.append(str(remove_control_chars(line)))
    

def remove_control_chars(s):        #去除任务中不可见字符（其实主要是为了去除换行）
    control_chars = ''.join(map(chr, list(range(0,32)) + list(range(127,160))))
    control_char_re = re.compile('[%s]' % re.escape(control_chars))
    s = control_char_re.sub('', s)
    return s

def random_md5():

    while True:
        seed = "1234567890abcdefghijklmnopqrstuvwxyz"
        sa = []
        for i in range(16):
            sa.append(random.choice(seed))
        salt = ''.join(sa).encode('UTF-8')
        md5 = hashlib.md5(salt).hexdigest()
        if md5 not in BUMBLEIDLIST:
            break
    return md5

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=18888)
