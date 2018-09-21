# -*- coding: UTF-8 -*-
import os
import urllib.request
from  urllib import error
import time

import socket
socket.setdefaulttimeout(20)

import requests

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
        self.ENCODING = 'utf-8'
        self.isContinue = True#某个手机号获取失败的时候，判断要不要继续获取下一个

        self.loginUrl = 'this is base-loginUrl'
        self.phoneUrl = 'this is base-phoneUrl'
        self.releaseUrl = 'this is base-releaseUrl'


    def getToken(self):
        print(' 正在获取token ',end="")
        getTokenOk = False
        try:
            fr1 = urllib.request.urlopen(self.loginUrl,timeout=2)
            data=fr1.readline()
            idata=str(data, encoding = self.ENCODING)
            token = self.tokenResDealer(idata)
            if token:
                self.tokenSetter(token)
                getTokenOk = True
            else:
                self.TOKEN_FAILED_REASON = idata
        except error.HTTPError as e:
	        print (e.code)
        except error.URLError as e:
	        print (e.reason)
        finally:
            fr1.close()
        return True if getTokenOk else False

    #token处理器，从接口返回的数据中提取需要的token ，子类根据需要去实现
    def tokenResDealer(self, idata):
        pass

    #token设置器，获取token以后，需要做的一些事情，主要是用于phoneUrl和releaseUrl的更新，子类具去实现
    def tokenSetter(self, token):
        pass
    
    def getPhone(self):
            print(' 正在获取手机号 ')
            num = 0
            totalNum = 0
            succeNum = 0
            tmpphones = set()
            while totalNum < self.count:
                getPhoneOk = False
                try:
                    time.sleep(self.sleeptime)
                    fr2 = urllib.request.urlopen(self.phoneUrl,timeout=2)
                    # print('PHONEURL:',self.phoneUrl)
                    data = fr2.readline()
                    idata = data.decode(self.ENCODING)
                    phone = self.phoneResDealer(idata)
                    if phone:
                        # 获取
                        print('    ',self.succeNum+1,'/',totalNum+1,' :  获取到 '+phone,' ',end="")
                        tmpphones.add(phone)
                        self.releasePhone(phone)
                        self.save2file(phone) 
                        getPhoneOk = True   
                    else:
                        
                        print('    ',totalNum,' :  号码获取出错1:(可能是url拼接错误/返回值处理出错) '+idata,' ;',self.phoneUrl)   
                        print('continue?:',self.isContinue)
                        if not self.isContinue:
                            break             
                        time.sleep(self.sleeptime*3)#获取失败，且不停止的话，先休息个3倍睡眠时间
                except error.HTTPError as e:
                    print ('getphone httperror:',e.code)
                except error.URLError as e:
                    print ('getphone urlerror:',e.reason)
                except Exception as e:
                    print('  号码获取出错2(可能是服务器错误):',e)
                    print('  重新登录ing...')
                    self.getToken()
                finally:
                    fr2.close()
                totalNum += 1
                
            self.phones = list(tmpphones)
            return True if getPhoneOk else   False

    #手机号处理器，从接口返回的数据中提取需要的手机号 子类根据需要去实现
    def phoneResDealer(self, idata):
        pass

    #存储文件
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
        print(' 正在释放 ',end="")
        self.phoneReleaseDealer(phone)#重新处理一下释放url
        releaseOk = False
        attemps = 0#尝试次数
        while attemps < 3:
            try:
                time.sleep(self.sleeptime)
                fr3 = urllib.request.urlopen(self.releaseUrl,timeout=2)
                data = fr3.readline()
                idata = data.decode(self.ENCODING)
                release = self.releaseResDealer(idata)
                if release:
                    releaseOk =  True
                else:
                    print('释放出错1（可能是url拼接错误/返回值处理错）：',idata,'; ',self.releaseUrl)
                    if not self.isContinue:
                        break
            except error.HTTPError as e:
                print ('release httperror:',e.code)
            except error.URLError as e:
                print ('releasee urlerror:',e.reason)
            except Exception as e:
                print('  释放出错2(可能是服务器出错):',e)
            finally:
                fr3.close()
            if releaseOk:
                print(' ok ',end="")
                break#释放成功，停止循环
            else:
                print(' 释放出错,尝试 ',attemps,end="")#释放出错，则再试
                time.sleep(self.sleeptime*2)
                attemps += 1
        return True if releaseOk else False
    
    def releaseResDealer(self, idata):
        pass


    #释放之前拼接释放链接 子类根据需要去实现
    def phoneReleaseDealer(self,phone):
        pass        