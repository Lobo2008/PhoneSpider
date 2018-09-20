# -*- coding: UTF-8 -*-
import os
import urllib.request
from  urllib import error
import time

import socket
socket.setdefaulttimeout(20)
from Base import Base

isLocalTest = True

"""
官方网站    http://www.91ma.me/
    获取账号    http://api.fxhyd.cn/UserInterface.aspx?action=getaccountinfo&token=TOKEN

    获取号码    http://api.fxhyd.cn/UserInterface.aspx?action=getmobile&token=TOKEN&itemid=项目编号&excludeno=排除号段
    释放号码    http://api.fxhyd.cn/UserInterface.aspx?action=release&token=TOKEN&itemid=项目编号&mobile=手机号码
"""
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
        self.sleeptime = 5
        self.TOKEN_FAILED_REASON = ''
        self.ENCODING = 'utf-8'
        self.isContinue = True

        self.loginUrl = 'http://api.fxhyd.cn/UserInterface.aspx?action=login&username='+self.name+'&password='+self.password
        self.phoneUrl = 'http://api.fxhyd.cn/UserInterface.aspx?action=getmobile&itemid='+self.ItemId
        
        self.releaseUrl_ori = 'http://api.fxhyd.cn/UserInterface.aspx?action=release&itemid='+self.ItemId
        self.releaseUrl = ""

    #token处理器，从接口返回的数据中提取需要的token  success|007214108761d8ac768e9c61085bc3b244f0a1ef
    def tokenResDealer(self, idata):
        if idata[:7] == 'success':
            return idata[8:]
        return False

    #token设置器，获取token以后，还需要将获取电话号码的phoneUrl更新
    def tokenSetter(self, token):
        self.token =  token
        self.phoneUrl = self.phoneUrl+'&token='+self.token

    #手机号处理器，从接口返回的数据中提取需要的手机号 succes|13145678888
    def phoneResDealer(self, idata):
        if idata[:7] == 'success':
            return idata[8:] 
        return False

    #释放之前拼接释放链接
    def phoneReleaseDealer(self,phone):
        self.releaseUrl = self.releaseUrl_ori+'&token='+self.token+'&mobile='+phone

    def releaseResDealer(self, idata):
        # success  释放出错会返回数字 ，比如  2007  表示早就已经被释放了
        if idata == 'success':
            return True
        return False


    def spider(self):
        tokenrs = self.getToken()
        if tokenrs:
            print('     token是: ',self.token)
            self.getPhone()
            print(' 共获取到:',str(len(self.phones))+' 个手机号')
        else:
            print(' 获取token失败（可能原因：账号失效/utf8解码出错）',self.TOKEN_FAILED_REASON)
        

