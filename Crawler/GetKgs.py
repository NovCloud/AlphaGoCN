#!/usr/bin/env python
# -*- coding: utf-8 -*-
#####################################################################
#功能：爬取kgs网站上的棋谱数据，棋谱文件后缀为sgf                   #
#修改者:Yong Pi                                                     #
#创建者:XiuYuan Xu                                                  #
#当前版本Version 1.1                                                #
#使用环境:python3.X                                                 #
#Version1.0->Version1.1更新说明:                                    #
#     1.修改了一个bug,新增了判断文件路径是否存在，若否，则建立文件夹#
#　　 2.将原来的单线程处理改进为多线程处理，提高爬取效率近50倍      #
#     3.从原来的2.x迁移到python3.x(感谢JingLin Wang 提供提供迁移)   #
#     4.更新数据条目，现在已到1080页                                #
######################################################################
import re
from urllib import request as urllib2
import os
import _thread

url = 'http://www.gokgs.com/tournGames.jsp?id='
pattern1 = r'.*/(.*?).sgf'
pattern = r'<tr><td><a href="(.*?)">Download</a></td><td class="name">(.*?)</td><td class="name">(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td></tr>'
def getfile(y,x):
	now_url = y
	print(now_url)
	try:
	    response = urllib2.urlopen(now_url)
	    saveFile = open(x, 'wb')
	    saveFile.write(response.read())
	    saveFile.close()
	except Exception as e:
		print(e)

# 判断文件夹是否存在，不存在则建立
if os.path.exists('GO'):
    pass
else:
    os.makedirs('GO')
if os.path.exists('GO_info'):
    pass
else:
    os.makedirs('GO_info')
def getURL(num):
   for i in range(num,num+9):
      j=1
      while 1:
        try:
            N_url = url+str(i)+'&round='+str(j)
            response = urllib2.urlopen(N_url)
            restex =response.read()
            table = re.findall(pattern,str(restex))
            for x in range(0,len(table)):
                object = table[x]
                name = str(i)+'_'+str(j)+'_'+re.match(pattern1,object[0]).group(1)
                if os.path.exists('GO/'+name+'.sgf') and os.path.exists('GO_info/'+name+'.txt'):
                   continue
                getfile(object[0],'GO/'+name+'.sgf')
                listfile = open('GO_info/'+name+'.txt','a')
                for t in range(1,6):
                    listfile.write(object[t]+'\n')
                listfile.close()
            j = j+1
        except Exception as e:
            print(e)
            break
n=1 #计数线程数
for i in range(1,1080,10):
    try:
       _thread.start_new_thread(getURL,(i,))
       print("线程"+str(n)+"已成功创建!")
       n+=1
    except:
        print("Error:unable to start thread")
while 1:
    pass
