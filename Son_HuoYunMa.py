# -*- coding: UTF-8 -*-
import os
import urllib.request
from  urllib import error
import time

import socket
socket.setdefaulttimeout(20)
from Base import Base

isLocalTest = True

"""火云码
官网：http://47.94.137.238/api/
    登录：  http://47.94.137.238/api/do.php?action=loginIn&name=API账号&password=密码
        返回值：'1|a4248202f5b828d54792dffff4f02f1e'
    获取号码：http://47.94.137.238/api/do.php?action=getPhone&sid=项目id&token=登录时返回的令牌
        返回值  1|手机号        错误是  0|系统暂时没有 等情况
    释放号码：http://47.94.137.238/api/do.php?action=cancelRecv&sid=项目id&phone=要释放的手机号&token=登录时返回的令牌
            1|操作成功
"""

class Son_HuoYunMa(Base):
    def __init__(self, name, password):
        self.eventid = '43327' #evenid
        self.name = name
        self.password = password
        print('*****火云码解析（id='+self.eventid+'）*****')
        print('请输入需要获取的手机号数量: ')
        self.token = ''
        self.phones = []#手机号列表，仅用于统计
        self.ItemId = '998'
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
        self.sleeptime = 6
        self.TOKEN_FAILED_REASON = ''
        self.ENCODING = 'gbk'
        self.isContinue = True

        self.loginUrl = 'http://47.94.137.238/api/do.php?action=loginIn&name='+self.name+'&password='+self.password
        self.phoneUrl_ori = 'http://47.94.137.238/api/do.php?action=getPhone&sid='+self.ItemId
        self.phoneUrl = ''

        self.releaseUrl_ori = 'http://47.94.137.238/api/do.php?action=cancelRecv&sid='+self.ItemId
        self.releaseUrl = ''

    #token处理器，从接口返回的数据中提取需要的token  
    def tokenResDealer(self, idata):#'1|a4248202f5b828d54792dffff4f02f1e'
        if idata[:1] == '1':
            return idata[2:]
        return False

    #token设置器，获取token以后，还需要将获取电话号码的phoneUrl更新
    def tokenSetter(self, token):
        self.token =  token
        self.phoneUrl = self.phoneUrl_ori+'&token='+self.token

    #手机号处理器，从接口返回的数据中提取需要的手机号
    def phoneResDealer(self, idata):    # 正确 '1|15981603504|吉林 通化'
        if idata[:1]=='1':
            return idata[2:13]
        return False

    #释放之前拼接释放链接
    def phoneReleaseDealer(self,phone):
        self.releaseUrl = self.releaseUrl_ori+'&token='+self.token+'&phone='+phone

    #释放结果的判断
    def releaseResDealer(self, idata):
        # 错误 False:Session 过期   正确 1|操作成功
        if idata[:1]=='1':
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
        
