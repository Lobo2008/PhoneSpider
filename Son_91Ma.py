# -*- coding: UTF-8 -*-
import os
import urllib.request
from  urllib import error
import time

import socket
socket.setdefaulttimeout(20)
from Base import Base

isLocalTest = True


class Son_91Ma(Base):
    def __init__(self, name, password):
        self.eventid = '43312' #evenid
        self.name = name
        self.password = password
        print('*****91码解析（id='+self.eventid+'）*****')
        print('请输入需要获取的手机号数量: ')
        self.token = ''
        self.phones = []#手机号列表，仅用于统计
        self.ItemId = '33'
        self.count = int(input())
        if isLocalTest:
            self.root = '/Users/lobo/Documents/Code/PhoneDecode' #根目录
        else:
            self.root = os.getcwd().replace('\\','/')#对Windows下的路径进行处理
        self.path = self.root+'/'+self.eventid

        if not os.path.exists(self.path):
            os.mkdir(self.path)

        self.exists = set([phone.replace('.txt','') for phone in os.listdir(self.path)])#目前已经存在的手机号列表
        self.succeNum = 0#成功的数量，以存储为准
        self.sleeptime = 10
        self.TOKEN_FAILED_REASON = ''
        self.ENCODING = 'utf-8'
        self.isContinue = True

        self.loginUrl = 'http://api.fxhyd.cn/UserInterface.aspx?action=login&username='+self.name+'&password='+self.password
        self.phoneUrl = 'http://api.fxhyd.cn/UserInterface.aspx?action=getmobile&token='+self.token+'&itemid='+self.ItemId
        self.releaseUrl = 'http://api.fxhyd.cn/UserInterface.aspx?action=release&token='+self.token+'&itemid='+self.ItemId+'&mobile='

    #token处理器，从接口返回的数据中提取需要的token  success|007214108761d8ac768e9c61085bc3b244f0a1ef
    def tokenResDealer(self, idata):
        if idata[:7] == 'success':
            return idata[8:]
        return False

    #手机号处理器，从接口返回的数据中提取需要的手机号 succes|13145678888
    def phoneResDealer(self, idata):
        if idata[:7] == 'success':
            return idata[8:] 
        return False

    #释放之前拼接释放链接
    def phoneReleaseDealer(self,phone):
        self.releaseUrl = self.releaseUrl+phone

    def spider(self):
        tokenrs = self.getToken()
        if tokenrs:
            print('     token是: ',self.token)
            self.phoneUrl = 'http://api.fxhyd.cn/UserInterface.aspx?action=getmobile&token='+self.token+'&itemid='+self.ItemId
            self.getPhone()
            print(' 共获取到:',str(len(self.phones))+' 个手机号')
        else:
            print(' 获取token失败（可能原因：账号失效/utf8解码出错）',self.TOKEN_FAILED_REASON)
        

