# -*- coding: UTF-8 -*-
import os
import urllib.request
from  urllib import error
import time

import socket
socket.setdefaulttimeout(20)

isLocalTest = True

class Base:

    def __init__(self, name, password):
        self.eventid = 'base event id' #evenid
        self.name = name
        self.password = password
        self.token = ''
        self.phones = []#手机号列表
        self.ItemId = 'base itemid'
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
        self.sleeptime = 5
        self.TOKEN_FAILED_REASON = ''

        self.loginUrl = 'this is base-loginUrl'
        self.phoneUrl = 'this is base-phoneUrl'
        self.releasUrl = 'this is base-releaseUrl'


    def getToken(self):
        print(' 正在获取token ',end="")
        getTokenOk = False
        try:
            fr = urllib.request.urlopen(self.loginUrl)
            data=fr.readline()
            idata=str(data, encoding = "utf-8")# 
            token = self.tokenResDealer(idata)
            if token:
                self.token =  token
                getTokenOk = True
            else:
                self.TOKEN_FAILED_REASON = idata
        except error.HTTPError as e:
	        print (e.code)
        except error.URLError as e:
	        print (e.reason)
        fr.close()
        return True if getTokenOk else False

    def tokenResDealer(self, idata):
        pass

    def getPhone(self):
            # http://kapi.yika66.com:20153/User/getPhone?ItemId=项目ID&token=登陆token
            print(' 正在获取手机号 ')
            num = 0
            tmpphones = set()
            while num < self.count:
                getPhoneOk = False
                try:
                    fr = urllib.request.urlopen(self.phoneUrl)
                    data = fr.readline()
                    idata = str(data, encoding = "utf-8")
                    fr.close()
                    phone = self.phoneResDealer(idata)
                    if phone:
                        # 获取
                        print('    ',num+1,' :  获取到 '+phone,' ',end="")
                        tmpphones.add(phone)
                        self.releasePhone(phone)
                        self.save2file(phone) 
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

    def phoneResDealer(self, idata):
        pass

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
        self.phoneReleaseDealer(phone)#重新处理一下释放url
        releaseOk = False
        attemps = 0#尝试次数
        while attemps < 3:
            try:
                fr = urllib.request.urlopen(self.releasUrl)
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

    def phoneReleaseDealer(self,phone):
        pass        
        
    def spider(self):
        # tokenrs = self.getToken()
       
        tokenrs = True
        if tokenrs:
            print('     token是: ',self.token)

            self.getPhone()
            print('获取到:',str(len(self.phones))+' 个手机号')
        else:
            print(' 获取token失败（可能原因：账号失效/utf8解码出错）',self.TOKEN_FAILED_REASON)
       

