# -*- coding: UTF-8 -*-
import os
import urllib.request
from urllib import error
import time
import socket
socket.setdefaulttimeout(20)



os.chdir('/Users/lobo/Documents/Code/PhoneSpider')


i=input("请输入获取数:")#43356
j=1
try:
	file=urllib.request.urlopen('http://xapi.yzm7.com/Login?uName=test_qq&pWord=12345678&Developer=VY7%2bHDp7FRgdst3yE6zHuQ%3d%3d')
except error.HTTPError as e:
	print (e.code)
except error.URLError as e:
	print (e.reason)
data=file.readline()
idata=str(data, encoding = "utf-8")
idata = idata[:idata.index('&')]
print('toekenrs:',idata)
if len(idata) == 32:
	token=idata
	print("token:"+token)
else:
	print("获取token失败")
file.close()
	
while j<=int(i):
	
	try:
		file1=urllib.request.urlopen('http://xapi.yzm7.com/getPhone?ItemId=2064&token='+token)
	except error.HTTPError as e:
		print (e.code)
	except error.URLError as e:
		print (e.reason)
	except:
		pass
	try:
		data2=file1.readline()
		iphone=str(data2, encoding = "utf-8")
	except:
		pass
	print('phoners:',iphone)
	file1.close()
	#if iphone[:1] == '1':
    # if  iphone[:5] != 'False' and len(iphone) > 11:
    # if False:
	if iphone[:5] != 'False' and len(iphone) > 11:
		phone = iphone[:11]
	    # phone = iphone[:11]
		b = os.getcwd() + '/dataout/'
		f1=open(b+phone+'.txt', "w")
		f1.write(phone)
		f1.close()
		#a = os.path.dirname(os.getcwd()) + '\\phonenumber\\'
		#f2=open(a+phone+'.txt', "w")
		#f2.write(phone)
		#f2.close()
	try:
		releaseUrl = 'http://xapi.yzm7.com/releasePhone?token='+token+'&phoneList='+phone+'-2064;'
		file2=urllib.request.urlopen(releaseUrl)
	except error.HTTPError as e:
		print (e.code)
	except error.URLError as e:
		print (e.reason)
	except:
		pass
	try:
		data3=file2.readline()
		ufile=str(data3,encoding = "utf-8")
	except:
		pass
	print('releaseUrl:',releaseUrl)
	print("releasers:",ufile)
	file2.close()
	if ufile[:5] == 'False':

		print('重新获取token...')
		try:
			rfile=urllib.request.urlopen('http://xapi.yzm7.com/Login?uName=test_qq&pWord=12345678&Developer=VY7%2bHDp7FRgdst3yE6zHuQ%3d%3d')
		except error.HTTPError as e:
			print (e.code)
		except error.URLError as e:
			print (e.reason)
		except:
			pass
		data=rfile.readline()
		idata=str(data, encoding = "utf-8")
		token=idata[2:]
		rfile.close()
	j=j+1
	print("执行获取操作次数:"+str(j-1))
	time.sleep(3)
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
	
	
	
