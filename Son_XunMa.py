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
官网：http://www.xunma.net/
    登录：  http://xapi.xunma.net/Login?uName=用户名&pWord=密码&Developer=开发者参数
        返回：  登录token&账户余额&最大登录客户端个数&最多获取号码数&单个客户端最多获取号码数&折扣
    获取号码： http://xapi.xunma.net/getPhone?ItemId=项目ID&token=登陆token
        返回：  13112345678; 正确
                False: Session 过期
    释放号码：http://xapi.xunma.net/releasePhone?token=登陆token&phoneList=phone-itemId;phone-itemId;

"""
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
        self.sleeptime = 3
        self.TOKEN_FAILED_REASON = ''
        self.ENCODING = 'gbk'
        self.isContinue = True

        self.loginUrl = 'http://xapi.xunma.net/Login?uName='+ self.name +'&pWord='+ self.password +'&Developer=8pRH3yF8n2Vz23Hfd%2b%2bHuQ%3d%3d'
        self.phoneUrl_ori = 'http://xapi.xunma.net/getPhone?ItemId='+self.ItemId
        self.phoneUrl = ''

        self.releaseUrl_ori = 'http://xapi.xunma.net/releasePhone?'
        self.releaseUrl = ''#每次都要用releaseUrl_ori来拼接新的号码
        

    #token处理器，从接口返回的数据中提取需要的token  mfvsx0JjTVlWmc2vTC0JF5ge90JmDr79&4.706&20&200&20&0.98&0
    def tokenResDealer(self, idata):
        return idata[:idata.index('&')]

    #token设置器，获取token以后，还需要将获取电话号码的phoneUrl，释放号码的releaseUrl用token更新
    def tokenSetter(self, token):
        self.token =  token
        self.phoneUrl = self.phoneUrl_ori+'&token='+self.token

    #手机号处理器，从接口返回的数据中提取需要的手机号 succes|13145678888
    def phoneResDealer(self, idata):
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


    def releaseResDealer(self, idata):
        #RES&3658&13285704607[End]
        #False:信息不完整!
        if idata[:5] == 'False':
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
        

