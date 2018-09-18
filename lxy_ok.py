# -*- coding: UTF-8 -*-
import os
import urllib.request
from urllib import error
import time
import socket
socket.setdefaulttimeout(20)
i=input("请输入获取数:")
j=1
try:#http://api.fxhyd.cn/UserInterface.aspx?action=login&username=hzw12356&password=123456qwe'
	file=urllib.request.urlopen('http://api.fxhyd.cn/UserInterface.aspx?action=login&username=hzw12356&password=123456qwe')
except error.HTTPError as e:
	print (e.code)
except error.URLError as e:
	print (e.reason)
data=file.readline()
idata=str(data, encoding = "utf-8")
if idata[:7] == 'success':
	token =  idata[8:]
	print("token:"+token)
else:
	print("获取token失败")
file.close()
	
while j<=int(i):
	
	try:#http://api.fxhyd.cn/UserInterface.aspx?action=getmobile&token='+self.token+'&itemid='+self.ItemId
		file1=urllib.request.urlopen('http://api.fxhyd.cn/UserInterface.aspx?action=getmobile&token='+token+'&itemid=33')
	except error.HTTPError as e:
		print (e.code)
	except error.URLError as e:
		print (e.reason)
	try:
		data2=file1.readline()
		iphone=str(data2, encoding = "utf-8")
	except:
		pass
	phone=iphone[8:]
	print("phone:"+phone)
	file1.close()
	b = '/Users/lobo/Documents/Code/PhoneDecode/lxy/'
	f1=open(b+phone+'.txt', "w")
	f1.write(phone)
	try:#http://api.fxhyd.cn/UserInterface.aspx?action=release&token='+self.token+'&itemid='+self.ItemId+'&mobile='+phone
		file2=urllib.request.urlopen('http://api.fxhyd.cn/UserInterface.aspx?action=release&token='+token+'&itemid=33&mobile='+phone)
	except error.HTTPError as e:
		print (e.code)
	except error.URLError as e:
		print (e.reason)
	try:
		data3=file2.readline()
		ufile=str(data3,encoding = "utf-8")
	except:
		pass
	print("return："+ufile)
	file2.close()
	j=j+1
	time.sleep(5)
def visitDir(path):
    if not os.path.isdir(path):
        print('Error: "', path, '" is not a directory or does not exist.')
        return
    else:
        global x
        try:
            for lists in os.listdir(path):
                #sub_path = os.path.join(path, lists)
                x += 1
                #print('No.', x, ' ', sub_path)
                #if os.path.isdir(sub_path):
                    #visitDir(sub_path)
        except:
            pass
 
 
if __name__ == '__main__':
    x = 0
    visitDir(b)
    print('获取号码总数: ', x)
	
	
	
