from lib.showprocess import ShowProcess
import threading
import time
import os

class WorkeBee:
    def __init__(self,SCRIPT,TASK,thread_num=15):
        self.script = SCRIPT.BumbleBeeWorker #此处函数名务必正确
        self.is_finish=False
        self.g_index=0
        self.g_total=len(TASK)
        self.threads=[]
        self.result=[]
        self.lock=threading.Lock()
        self.thread_num = thread_num
        self.tasklist = TASK
        self.process_bar = ShowProcess(self.g_total, '所有任务已完成') # 进度条方法初始化
        msg = "WorkeBee正在启动，当前任务进度："
        print(msg)
    
    def workeralive(self):
        woker_alive_number = 0
        for i in self.threads:
            if i.isAlive():
                woker_alive_number += 1
        return woker_alive_number

    def work(self,i):
        while True:
            # if self.is_finish: #如果结果标志，则退出
            #     print(i,"exit")
            #     break

            if self.g_index >= len(self.tasklist):  #这说明所有的任务已经被分配完，子线程可以退出了
                # print(i,self.g_index,self.workeralive(),"exit")
                break

            self.lock.acquire()             #取任务上锁
            try:
                eachtask = self.tasklist[self.g_index] #获取任务中其中一个
            except:
                break
            self.g_index += 1               #获取任务成功后，增加序号
            self.lock.release()             #释放获取锁

            achievement = {eachtask:self.script(eachtask)}
            self.result.append(achievement)
            self.process_bar.show_process()

    def start_threads(self):
        for i in range(self.thread_num):
            t = threading.Thread(target=self.work,args=(i,))
            self.threads.append(t)
        for t in self.threads:
            t.start()
        # for t in self.threads: #此处我们就不使用阻塞的方法了
        #     t.join()

    def run(self):
        self.start_threads()

    def get_result(self): 
        while True:
            time.sleep(0.1)
            if self.workeralive()==0: #任务已经完成，设置finish标志位为true
                self.is_finish = True
            if self.is_finish:
                return self.result
