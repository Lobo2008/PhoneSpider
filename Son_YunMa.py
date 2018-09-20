# -*- coding: UTF-8 -*-
import os
import urllib.request
from  urllib import error
import time

import socket
socket.setdefaulttimeout(20)
from Base import Base

isLocalTest = False

"""
官网：http://www.yzm7.com/
    登录：  http://xapi.yzm7.com/Login?uName=用户名&pWord=密码&Developer=开发者参数
        返回值：登录token&账户余额&最大登录客户端个数&最多获取号码数&单个客户端最多获取号码数&折扣
    获取号码：http://xapi.yzm7.com/getPhone?ItemId=项目ID&token=登陆token
        返回值  13112345678;13698763743;13928370932;
    释放号码：http://xapi.yzm7.com/releasePhone?token=登陆token&phoneList=phone-itemId;phone-itemId;

"""

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

        self.loginUrl = 'http://xapi.yzm7.com/Login?uName='+self.name+'&pWord='+self.password+'&Developer=VY7%2bHDp7FRgdst3yE6zHuQ%3d%3d'
        self.phoneUrl = 'http://xapi.yzm7.com/getPhone?ItemId='+self.ItemId
        
        self.releaseUrl_ori = 'http://xapi.yzm7.com/releasePhone?'
        self.releaseUrl = ''

    #token处理器，从接口返回的数据中提取需要的token  
    def tokenResDealer(self, idata):
        return idata[:idata.index('&')]

    #token设置器，获取token以后，还需要将获取电话号码的phoneUrl更新
    def tokenSetter(self, token):
        self.token =  token
        self.phoneUrl = self.phoneUrl+'&token='+self.token

    #手机号处理器，从接口返回的数据中提取需要的手机号
    def phoneResDealer(self, idata):    #错误： False:Session 过期  正确 17123209468;
        if idata[:5]=='False':#获取号码失败，可能是没有项目，所以这里还要继续处理一下
            if '过期' in idata:#Session过期，需要重新登录一下
                print('Session过期，重新登录...')
                self.getToken()
            return False
        elif len(idata) > 11:
            return idata[:11] 
        return False

    #释放之前拼接释放链接
    def phoneReleaseDealer(self,phone):
        self.releaseUrl = self.releaseUrl_ori+'&token='+self.token+'&phoneList='+phone+'-'+self.ItemId+';'

    #释放结果的判断
    def releaseResDealer(self, idata):
        # 错误 False:Session 过期   正确 RES&2063&17223209468[End]
        if idata[:5]=='False':
            return False
        return True


    def spider(self):
        tokenrs = self.getToken()
        if tokenrs:
            print('     token是: ',self.token)
            self.getPhone()
            print(' 共获取到:',str(len(self.phones))+' 个手机号')
        else:
            print(' 获取token失败（可能原因：账号失效/utf8解码出错）',self.TOKEN_FAILED_REASON)
        
