import threading
import os
from queue import Queue
from multiprocessing import Process
import sys, getopt, socket
from multiprocessing.pool import Pool
import re
import json
import time
import copy
from concurrent.futures import ThreadPoolExecutor
from multiprocessing.dummy import Pool as ThreadPool
from functools import partial
import fire
import subprocess

class NetworkTestThread(threading.Thread):
    '''
     网络测试类
    '''
    def __init__(self,thread_id,ipinfo_queue,cmd):
        super().__init__()
        self.thread_id = thread_id
        self.ipinfo_queue = ipinfo_queue
        self.cmd = cmd

    def run(self):
        '''
        重写run 方法
        '''
        print(f'启动线程: {self.thread_id}')
        if self.cmd == 'ping':
            self.pingtest()
        elif self.cmd == 'tcp':
            self.tcptest()
    
    def pingtest(self):
        while True:
            if self.ipinfo_queue.empty():
                break
            else:
                ipinfo = self.ipinfo_queue.get()
                print('测试线程为：',self.thread_id,'测试ip为：',ipinfo)

                try:
                    re = subprocess.run(["ping",ipinfo[0], "-t", "2"],
                            capture_output=True)
                    if re.returncode == 0:
                        print(ipinfo[0])
                except Exception as e:
                    print(e)
                    print("Something went wrong with your ping program!")
    
    def tcptest(self):
        while True:
            if self.ipinfo_queue.empty():
                break
            else:
                ipinfo = self.ipinfo_queue.get()
                print('测试线程为：',self.thread_id,'测试ip为：',ipinfo)

                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(2)

                # connect to remote host
                try:
                    return_code = s.connect_ex(ipinfo)
                except OSError as e:
                    print('OS Error:', e)
        
                if return_code == 0:
                    print("Connected.")
                else:
                    print('Unable to connect.')


def test(n,f,ip):
    ipinfo_queue = Queue(65536)
    network_thread = []
    if f == 'ping':
        start_ip, stop_ip = ip.split('-')
        start_last_num = start_ip.split('.')[-1]
        stop_last_num = stop_ip.split('.')[-1]
        start_head = start_ip.rstrip(start_last_num).rstrip('.')
        seed = [start_head + '.' + str(num) for num in range(int(start_last_num), int(stop_last_num)+1)]
        
        for ipinfo in seed:
            ipinfo_queue.put((ipinfo,80))
        
        for thread_id in range(1,n):
            thread = NetworkTestThread(thread_id, ipinfo_queue,f)
            thread.start()
            network_thread.append(thread)

    elif f == 'tcp':
        seed = [(ip, port) for port in range(0, 65536)]
        for ipinfo in seed:
            ipinfo_queue.put(ipinfo)
        
        for thread_id in range(1,n):
            thread = NetworkTestThread(thread_id, ipinfo_queue,f)
            thread.start()
            network_thread.append(thread)

    for t in network_thread:
        t.join()


fire.Fire(test)
