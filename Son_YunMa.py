# -*- coding: UTF-8 -*-
import os
import urllib.request
from  urllib import error
import time

import socket
socket.setdefaulttimeout(20)
from Base import Base

isLocalTest = False


class Son_YunMa(Base):
    def __init__(self, name, password):
        self.eventid = '43356' #evenid
        self.name = name
        self.password = password
        print('*****云码解析（id='+self.eventid+'）*****')
        print('请输入需要获取的手机号数量: ')
        self.token = ''
        self.phones = []#手机号列表，仅用于统计
        self.ItemId = '2064'
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
        self.ENCODING = 'gb2312'

        self.loginUrl = 'http://xapi.yzm7.com/Login?uName='+self.name+'&pWord='+self.password+'&Developer=VY7%2bHDp7FRgdst3yE6zHuQ%3d%3d'
        self.phoneUrl = 'http://xapi.yzm7.com/getPhone?ItemId='+self.ItemId
        self.releaseUrl = 'http://xapi.yzm7.com/releasePhone?'

    #token处理器，从接口返回的数据中提取需要的token  
    def tokenResDealer(self, idata):
        return idata[:idata.index('&')]

    #token设置器，获取token以后，还需要将获取电话号码的phoneUrl，释放号码的releaseUrl用token更新
    def tokenSetter(self, token):
        self.token =  token
        self.phoneUrl = self.phoneUrl+'&token='+self.token
        self.releaseUrl = self.releaseUrl+'&token='+self.token

    #手机号处理器，从接口返回的数据中提取需要的手机号
    def phoneResDealer(self, idata):
        if idata[:5]=='False':#获取号码失败，可能是没有项目，所以这里还要继续处理一下
            self.isContinue = False
            return False
        elif len(idata) > 11:
            return idata[:11] 
        return False

    #释放之前拼接释放链接
    def phoneReleaseDealer(self,phone):
        self.releaseUrl = self.releaseUrl+'&phoneList='+phone+'-'+self.ItemId+';'

    def spider(self):
        tokenrs = self.getToken()
        if tokenrs:
            self.getPhone()
            print(' 共获取到:',str(len(self.phones))+' 个手机号')
        else:
            print(' 获取token失败（可能原因：账号失效/utf8解码出错）',self.TOKEN_FAILED_REASON)
        
