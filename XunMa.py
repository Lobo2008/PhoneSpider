# -*- coding: UTF-8 -*-
import os
import urllib.request
from  urllib import error
import time

import socket
socket.setdefaulttimeout(20)


isLocalTest = False

class XunMa:

    def __init__(self, name, password):
        self.eventid = '43335' #evenid
        self.name = name
        self.password = password
        print('*****讯码解析（id='+self.eventid+'）*****')
        print('请输入需要获取的手机号数量: ')

        self.token = ''
        self.phones = []#手机号列表
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

    def getToken(self):
        print(' 正在获取token ',end="")
        loginUrl = 'http://xapi.xunma.net/Login?uName='+ self.name +'&pWord='+ self.password +'&Developer=2'
        getTokenOk = False
        try:
            fr = urllib.request.urlopen(loginUrl)
            data=fr.readline()
            idata=str(data, encoding = "utf-8")
            if idata:
                self.token =  idata[:idata.index('&')]
                getTokenOk = True
            else:
                self.TOKEN_FAILED_REASON = idata
        except error.HTTPError as e:
	        print (e.code)
        except error.URLError as e:
	        print (e.reason)
        fr.close()
        return True if getTokenOk else False

            
    def getPhone(self):
            # http://xapi.xunma.net/getPhone?ItemId=项目ID&token=登陆token
            print(' 正在获取手机号 ')
            phoneUrl = phoneUrl = 'http://xapi.xunma.net/getPhone?ItemId='+self.ItemId+'&token='+self.token+'&Count=1'
            num = 0
            tmpphones = set()
            while num < self.count:
                getPhoneOk = False
                try:
                    fr = urllib.request.urlopen(phoneUrl)
                    data = fr.readline()
                    idata = str(data, encoding = "utf-8")
                    if len(idata) > 11:
                        # 获取，源数据格式 13216418039;
                        print('    ',num+1,' :  获取到 '+idata[:11],' ',end="")
                        tmpphones.add(idata[:11])
                        self.releasePhone(idata[:11])
                        self.save2file(idata[:11]) 
                        getPhoneOk = True   
                    else:
                        print('    ',num,' :  获取失败 '+idata,' ',end="")                
                except error.HTTPError as e:
                    print (e.code)
                except error.URLError as e:
                    print (e.reason)
                num += 1
                fr.close()#每次获取完一个手机号都要关闭链接
                time.sleep(self.sleeptime)
            self.phones = list(tmpphones)
            return True if getPhoneOk else   False



    def save2file(self, phone):
        print(' 正在存储 ',end="")

        if phone not in self.exists:
            try:
                fr = open(self.path+'/'+phone+'.txt','w')  
                fr.write(phone)
                fr.close()
                self.succeNum += 1
                self.exists.add(phone)
                print('   ok! ')
            except:
                print('   失败 ')
        else:
            print('     已存在')


    def releasePhone(self, phone):
        # http://xapi.xunma.net/releasePhone?token=登陆token&phoneList=phone-itemId;phone-itemId
        print(' 正在释放 ',end="")
        phone = phone+'-'+self.ItemId
        releasUrl = 'http://xapi.xunma.net/releasePhone?token='+self.token+'&phoneList='+phone
        releaseOk = False
        attemps = 0#尝试次数
        while attemps < 3:
            try:
                fr = urllib.request.urlopen(releasUrl)
                releaseOk =  True
            except error.HTTPError as e:
                print (e.code)
            except error.URLError as e:
                print (e.reason)
            if releaseOk:
                print(' ok ',end="")
                break#释放成功，停止循环
            else:
                print(' 释放出错,尝试 ',attemps,end="")#释放出错，则再试
                time.sleep(self.sleeptime*2)
                fr.close()
                attemps += 1
        fr.close()
        return True if releaseOk else False
        
    def spider(self):
        tokenrs = self.getToken()
        if tokenrs:
            print('     token是: ',self.token)
            self.getPhone()
            print('获取到:',str(len(self.phones))+' 个手机号')
        else:
            print(' 获取token失败（可能原因：账号失效/utf8解码出错）',self.TOKEN_FAILED_REASON)
       

