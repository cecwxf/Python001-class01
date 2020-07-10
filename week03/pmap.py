# /usr/local/bin/python3 /Users/orion/python_test/homework/w3/pmap.py -n 4 -f ping -p 10.60.99.32-10.60.99.60 -w 1.txtimport time
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

inputArgs = {}
ipaddresses = []
usedport = []
ip_avalibale = ["127.0.0.1"]

dataqueue = Queue(100)

testresult = {
    "usedport" : [],
    "ipavailable" : []
}
def save_data():
    print('保存文件地址:'+inputArgs["savePath"])
    output = open(inputArgs["savePath"],mode= 'a+',encoding='utf-8')
    json.dump(testresult, output, ensure_ascii=False)

def check_port(ip, port=80):
    info = []
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        global ip_avalibale
        s.connect((ip, port))
        s.shutdown(2)
        print('%s:%d is used' % (ip, port))
        info = [(ip,port)]
        usedport.append(info)
        testresult["usedport"] = usedport
        # dataqueue.put(usedport)
        save_data()
        # return True
    except socket.error as e:
        print('%s:%d is unused' % (ip, port))
        # return False

def get_ping_result(ip_address,port):
    print("begin get_ping_result ip_address:",ip_address)
    testMethod = inputArgs["testMethod"]
    print('testmethod is',testMethod)
    if testMethod == 'ping':
        out = os.popen(f'{testMethod} {ip_address}','r', buffering=-1)
        result = out.readline()
        result = out.readline()
    elif testMethod == 'tcp':
        check_port(ip_address,port)
    if 'timeout' in result:
        print("不能 ping通",ip_address)
    elif 'time=' in result:
        global ip_avalibale
        print("可以 ping通",ip_address)
        ip_avalibale.append(ip_address)
        # return ip_avalibale
        testresult["ipavailable"] = ip_avalibale
        # print(ip_avalibale)
        save_data()

def get_inputopts():
    print("获取相关参数")
    opts,args = getopt.getopt(sys.argv[1:],'-n:-f:-p:-w:',['number=','fping=','ip'])
    for opt_name,opt_value in opts:
        if opt_name in ('-n','--numvber'):
            print("[*] 并发数量",opt_value)
            inputArgs["processNum"] = opt_value
        if opt_name in ('-f','--fping'):
            print("[*] 测试方式 ",opt_value)
            inputArgs["testMethod"] = opt_value
        if opt_name in ('-p','-ipaddr'):
            print("[*] ip范围 is ",opt_value)
            inputArgs["testIp"] = opt_value
        if opt_name in('-w'):
            print("[*] 保存到文件",opt_value)
            inputArgs["savePath"] = opt_value

if __name__ == '__main__':
    get_inputopts()

    # 进程并发数
    n = int(inputArgs["processNum"])
    p = Pool(n)

    #ping 的ip 数量
    ipRange = inputArgs['testIp']
    pi = re.compile(r'((([01]?\d?\d|2[0-4]\d|25[0-5])\.){3}([01]?\d?\d|2[0-4]\d|25[0-5]))');
    result = pi.findall(ipRange)

    ipaddresses.append(result[0][0])
    if(list(result).__len__() > 1):
        ipaddresses.append(result[1][0])
        iplen = int((result[1][3]))- int((result[0][3])) + 1
        ipaddresses.append(iplen)
    else:
        iplen = 1
    print("要测试的ip地址数量为:",iplen)
    # 要测试的ip地址范围
    print("要测试的ip地址范围为:", ipaddresses) 

    iplist = ipaddresses[0]

    ipstr = str(iplist).split('.')[0] + '.' + str(iplist).split('.')[1] + '.' + str(iplist).split('.')[2] + '.'
    ip_address = ipstr
    if "ping" == inputArgs["testMethod"]:
        for i in range(iplen):
            ipaddr = i + int(str(iplist).split('.')[-1])
            ip_address = (ipstr + str(ipaddr))
            print("ping 要测试的地址"+ip_address)
            p.apply_async(get_ping_result, args=(copy.deepcopy(ip_address),80,))
    elif "tcp" == inputArgs["testMethod"]:
        for i in range(iplen):
            ipaddr = i + int(str(iplist).split('.')[-1])
            ip_address = (ipstr + str(ipaddr))
            print("tcp 要测试的地址"+ip_address)
            for port in range(1024):
                p.apply_async(get_ping_result, args=(ip_address,port))
    
    # print(dataqueue.get())              
    p.close()
    p.join()  
