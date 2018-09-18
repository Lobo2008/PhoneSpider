# -*- coding: UTF-8 -*-
import os
import urllib.request
from  urllib import error
import time

import socket
socket.setdefaulttimeout(20)
from Base import Base

isLocalTest = False


class Son_XunMa(Base):
    def __init__(self, name, password):
        self.eventid = '43335' #evenid
        self.name = name
        self.password = password
        print('*****讯码解析（id='+self.eventid+'）*****')
        print('请输入需要获取的手机号数量: ')
        self.token = ''
        self.phones = []#手机号列表，仅用于统计
        self.ItemId = '3658'
        if isLocalTest:
            self.count = 3 #手机号的数量
            self.root = '/Users/lobo/Documents/Code/PhoneDecode' #根目录
        else:
            self.count = int(input())
            self.root = os.getcwd().replace('\\','/')#对Windows下的路径进行处理
        self.path = self.root+'/'+self.eventid

        if not os.path.exists(self.path):
            os.mkdir(self.path)

        self.exists = set([phone.replace('.txt','') for phone in os.listdir(self.path)])#目前已经存在的手机号列表
        self.succeNum = 0#成功的数量，以存储为准
        self.sleeptime = 10
        self.TOKEN_FAILED_REASON = ''
        self.loginUrl = 'http://xapi.xunma.net/Login?uName='+ self.name +'&pWord='+ self.password +'&Developer=2'
        self.phoneUrl = 'http://xapi.xunma.net/getPhone?ItemId='+self.ItemId+'&token='+self.token+'&Count=1'
        self.releasUrl = 'http://xapi.xunma.net/releasePhone?token='+self.token+'&phoneList='

    #token处理器，从接口返回的数据中提取需要的token  mfvsx0JjTVlWmc2vTC0JF5ge90JmDr79&4.706&20&200&20&0.98&0
    def tokenResDealer(self, idata):
        return idata[:idata.index('&')]
        

    #手机号处理器，从接口返回的数据中提取需要的手机号 succes|13145678888
    def phoneResDealer(self, idata):
        if len(idata) > 11:
            return idata[:11] 
        return False

    #释放之前拼接释放链接
    def phoneReleaseDealer(self,phone):
        self.releasUrl = self.releasUrl+phone+'-'+self.ItemId

    def spider(self):
        tokenrs = self.getToken()
        if tokenrs:
            print('     token是: ',self.token)
            self.phoneUrl = 'http://xapi.xunma.net/getPhone?ItemId='+self.ItemId+'&token='+self.token+'&Count=1'
            self.getPhone()
            print(' 共获取到:',str(len(self.phones))+' 个手机号')
        else:
            print(' 获取token失败（可能原因：账号失效/utf8解码出错）',self.TOKEN_FAILED_REASON)
        

