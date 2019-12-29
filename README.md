# BumbleBee

BumbleBee是一个分布式脚本运行程序，只需要向QueueBee提交脚本和任务，QueueBee会自动将脚本和任务下发给WorkeBee并收集运行结果。

# 当前版本V0.001

# 使用方法

## 配置

/start.py 中的QUEUEHOST配置为QueueBee的IP地址

/WorkeBee/lib/data.py中的QUEUEHOST配置为QueueBee的IP地址

需要分布式运行的脚本放置于/QueueBee/script.py中，函数名参考样例

任务文件放置于/QueueBee/task.txt中，每行为一个任务，参考样例

## 前置准备

QueueBee端启动/QueueBee/main.py

WorkeBee端启动/WorkeBee/main.py

## 下发任务

运行start.py，查看任务进度，任务结束后会保存至/QueueBee/result.txt中

## python脚本样例

```
import requests
import re

def BumbleBeeWorker(HOST): # 该函数名不可修改，接收一个字符串参数，你可以在函数内对其进行处理
    try:
        r = requests.get(HOST)
        r.encoding = 'utf-8'
        context = re.findall(r'<title>(.*?)</title>', r.text)
        if context != []:
            return context[0]
    except:
        return 0          #务必保证所有情况均有返回值，且要保证程序不会异常退出
```
