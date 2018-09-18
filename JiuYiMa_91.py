# -*- coding: UTF-8 -*-
import os
import urllib.request
from  urllib import error
import time

import socket
socket.setdefaulttimeout(20)


isLocalTest = False


class JiuYiMa_91:
    def __init__(self, name, password):
        self.eventid = '43312' #evenid
        self.name = name
        self.password = password
        print('*****极速接码解析（id='+self.eventid+'）*****')
        print('请输入需要获取的手机号数量: ')

        self.token = ''
        self.phones = []#手机号列表
        self.ItemId = '33'
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
        loginUrl = 'http://api.fxhyd.cn/UserInterface.aspx?action=login&username='+self.name+'&password='+self.password
        print(loginUrl)
        getTokenOk = False
        try:
            fr = urllib.request.urlopen(loginUrl)
            data=fr.readline()
            idata=str(data, encoding = "utf-8")
            if idata[:7] == 'success':
                self.token =  idata[8:]
                getTokenOk = True
            else:
                self.TOKEN_FAILED_REASON = idata
        except error.HTTPError as e:
	        print (e.code)
        except error.URLError as e:
	        print (e.reason)
        # fr.close()
        return True if getTokenOk else False

            
    def getPhone(self):
            # http://api.fxhyd.cn/UserInterface.aspx?action=getmobile&token=TOKEN&itemid=项目编号&excludeno=排除号段
            print(' 正在获取手机号 ')
            phoneUrl = 'http://api.fxhyd.cn/UserInterface.aspx?action=getmobile&token='+self.token+'&itemid='+self.ItemId
            num = 0
            tmpphones = set()
            while num < self.count:
                getPhoneOk = False
                try:
                    fr = urllib.request.urlopen(phoneUrl)
                    data = fr.readline()
                    idata = str(data, encoding = "utf-8")
                    if idata[:7] == 'success':
                        # 获取，源数据格式 success|17121324782
                        print('    ',num+1,' :  获取到 '+idata[8:],' ',end="")
                        tmpphones.add(idata[8:])
                        self.releasePhone(idata[8:])#释放
                        self.save2file(idata[8:]) #存储，是否要存，到save2file里面判断
                        getPhoneOk = True
                    else:
                         print('    ',num,' :  获取失败 '+idata,' ',end="")    
                except error.HTTPError as e:
                    print (e.code)
                except error.URLError as e:
                    print (e.reason)
                num += 1
                time.sleep(self.sleeptime)
            self.phones = list(tmpphones)
            fr.close()
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
        # http://api.fxhyd.cn/UserInterface.aspx?action=release&token=TOKEN&itemid=项目编号&mobile=手机号码
        print(' 正在释放 ',end="")
        phoneList = ";".join([phone+'-'+self.ItemId for phone in self.phones])+";"
        releasUrl = 'http://api.fxhyd.cn/UserInterface.aspx?action=release&token='+self.token+'&itemid='+self.ItemId+'&mobile='+phone
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
            phoners = self.getPhone()
            print(' 共获取到:',str(len(self.phones))+' 个手机号')
        else:
            print(' 获取token失败（可能原因：账号失效/utf8解码出错）',self.TOKEN_FAILED_REASON)
        

