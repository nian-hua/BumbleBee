# BumbleBee

BumbleBee是一个分布式脚本运行程序，只需要向QueueBee提交脚本和任务，QueueBee会自动将脚本和任务下发给WorkeBee并收集运行结果。

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
