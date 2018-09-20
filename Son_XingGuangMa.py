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
官网：http://www.20982098.com/
    登录：  http://120.78.95.181:9180/service.asmx/UserLoginStr?name=帐户名&psw=密码
        返回值：2632120F90A971D9FB4771D97D507BFD
    获取号码：http://120.78.95.181:9180/service.asmx/GetHM2Str?token=登陆令牌&xmid=项目编号&sl=号码数量&lx=号码类型&a1=省份&a2=城市&pk=专属对接KEY&ks=卡商Id编号&rj=作者帐户
        返回值  hm=13712345678
    释放号码：hhttp://120.78.95.181:9180/service.asmx/sfHmStr?token=登陆令牌&hm=手机号码
        返回值示例如： 1
"""

class Son_XingGuangMa(Base):
    def __init__(self, name, password):
        self.eventid = '43321' #evenid
        self.name = name
        self.password = password
        print('*****星光码解析（id='+self.eventid+'）*****')
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
        self.ENCODING = 'utf-8'
        self.isContinue = True

        self.loginUrl = 'http://120.78.95.181:9180/service.asmx/UserLoginStr?name='+self.name+'&psw='+self.password
        self.phoneUrl = 'http://120.78.95.181:9180/service.asmx/GetHM2Str?&xmid='+self.ItemId+'&sl=1&lx=0&ks=0&rj=abc123&a1=&a2=&pk='
        
        self.releaseUrl_ori = 'http://120.78.95.181:9180/service.asmx/sfHmStr?'
        self.releaseUrl = ''

    #token处理器，从接口返回的数据中提取需要的token  
    def tokenResDealer(self, idata):
        if len(idata) == 32:
            return idata
        return False

    #token设置器，获取token以后，还需要将获取电话号码的phoneUrl更新
    def tokenSetter(self, token):
        self.token =  token
        self.phoneUrl = self.phoneUrl+'&token='+self.token

    #手机号处理器，从接口返回的数据中提取需要的手机号
    def phoneResDealer(self, idata):    #hm=15981605846
        if idata[:2] == 'hm' and len(idata[3:]) == 11:
            return idata[3:]
        return False


    #释放之前拼接释放链接
    def phoneReleaseDealer(self,phone):
        self.releaseUrl = self.releaseUrl_ori+'&token='+self.token+'&hm='+phone

    #释放结果的判断
    def releaseResDealer(self, idata):
        # 错误 False:Session 过期   正确 RES&2063&17223209468[End]
        if idata != '1':
            return False
        return True


    def spider(self):
        tokenrs = self.getToken()
        if tokenrs:
            self.getPhone()
            print(' 共获取到:',str(len(self.phones))+' 个手机号')
        else:
            print(' 获取token失败（可能原因：账号失效/utf8解码出错）',self.TOKEN_FAILED_REASON)
        
