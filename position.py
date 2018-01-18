#coding:utf-8;
#qpy:2
#qpy:console
import json
import itchat
import re
from androidhelper import Android
import time
#from urllib.request import urlopen
from urllib2 import urlopen
import threading
import base64
import werobot
from itchat.content import *
import busstop
import datetime
import random
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

itchat.auto_login(enableCmdQR=True)
lastloc=0
mix_scope=0
i=0
QUIT=False
#station=[(30.467499,114.408628),(30.477924,114.409636),(30.480735,114.410108),(30.484702,114.410462),(30.489528,114.411138),(30.492301,114.411407),(30.496725,114.416175),(30.494936,114.423079),(30.492449,114.428841)]
#station=[(30.467499,114.408628),(30.476242,114.409567),(30.480818,114.410119),(30.484702,114.410462),(30.489422,114.411117),(30.492301,114.411407),(30.496725,114.416175),(30.494501,114.423904),(30.493554,114.425521)]
station=[(30.467499,114.408628),(30.47469,114.409661),(30.489422,114.411117),(30.492301,114.411407),(30.496725,114.416175),(30.494501,114.423904),(30.493554,114.425521)]
def locate():
    global station
    global mix_scope
    d=Android()  
    d.startLocating()  
   
    global lastloc
    loc=d.getLastKnownLocation().result['gps']
    #loc1=d.getLastKnownLocation().result
    #loc1=loc1.get('network',loc1.get('gps'))
    #print(loc)
    if loc==None:
        gps=d.getLastKnownLocation().result['network']
    elif loc==lastloc:
        gps=d.getLastKnownLocation().result['network']
    else:
        print('it is gps')
        gps=loc
    
    lngx=gps['longitude']
    lngy=gps['latitude']
    #lngx=loc1['longitude']
    #lngy=loc1['latitude']
    #print(loc1)
    #print(gps)
    lastloc=loc

    ur='http://apis.map.qq.com/ws/coord/v1/translate?locations='+str(lngy)+','+str(lngx)+'&type=1&key=Y5YBZ-VLZCX-EQR4Y-Z47JH-TZCHQ-TXF7H'
    f=urlopen(ur).read()
    f=json.loads(f)

    pos_lng=f['locations'][0]['lng']
    pos_lat=f['locations'][0]['lat']
    print(pos_lat)
    print(pos_lng)
              
    url='http://apis.map.qq.com/ws/geocoder/v1/?location='+str(pos_lat)+','+str(pos_lng)+'&key=Y5YBZ-VLZCX-EQR4Y-Z47JH-TZCHQ-TXF7H&get_poi=1'
    g=urlopen(url).read()
    g=json.loads(g)
    addr=g[u'result'][u'formatted_addresses'][u'recommend']
    mess=addr.encode('utf-8')
    print(mess)
    
    start=datetime.datetime.now()
    global i       
    #for i in range(mix_scope,7):
        #dis=busstop.get_distance_hav(pos_lat,pos_lng,station[i][0],station[i][1])*1000
        #print('dis'+str(dis))
    dis=busstop.distance(pos_lat,pos_lng,station[i][0],station[i][1])
    #print('tecent'+str(dis))
    if dis<=300:
        if i==0:
            werobot.sendmess('到达华夏理工')
            print('到达华夏理工')
            time.sleep(random.uniform(0,0.5))
            i=1
            huaxia_duration=busstop.huaxia2optical()
            werobot.sendmess('距离光谷天地约需'+huaxia_duration)
            print('距离光谷天地约需'+huaxia_duration) 
                #break
        elif i==1:
            werobot.sendmess('光谷天地到了')
            print('光谷天地到了')
            time.sleep(random.uniform(0,0.5))
            i=2
            optical_duration=busstop.optical2xinzhu()
            werobot.sendmess('距离新竹路约需'+optical_duration)
            print('距离新竹路约需'+optical_duration)
                #break
        elif i==2:
            werobot.sendmess('抵达新竹路')
            print('抵达新竹路')
            i=3
                #break
        elif i==3:
            werobot.sendmess('到达新南路')
            print('到达新南路')
            time.sleep(random.uniform(0,0.5))
            i=4
            xinnan_duration=busstop.xinnan2lanjing()
            werobot.sendmess('距离蓝晶国际约需'+xinnan_duration)
            print('距离蓝晶国际约需'+xinnan_duration)
                #break
        elif i==4:
            werobot.sendmess('蓝晶国际到了')
            print('蓝晶国际到了')
            i=5
                #break
        elif i==5:
            werobot.sendmess('到达光谷大道')
            print('到达光谷大道')
            i=6
                #break
        elif i==6:
            #werobot.sendmess('已到潮漫酒店')
            print('已到潮漫酒店')
                #break                

    end=datetime.datetime.now()   
    
    print (end-start)                
   
    
    #werobot.sendmess(addr)

#g=json.loads(g.decode())
 #   print(f['locations'][0]['lat'])
  #  print(f['locations'][0]['lng'])
    global timer
    tt=15
    #print(tt)
    timer=threading.Timer(tt,locate)
    timer.start()
    
def initial_station():
    while(1):
        currentime=time.strftime('%H:%M:%S',time.localtime(time.time()))
   # print(currentime)
        if currentime=='07:55:00':
            werobot.sendmess('发车了')
            [duration1,duration2]=busstop.start2huaxia_lanjing()
            time.sleep(random.uniform(0,0.3))
            mess1='距离华夏理工约需'+duration1
            #print(mess1)
            werobot.sendmess(mess1)
            time.sleep(random.uniform(0,0.3))
            werobot.sendmess('距离蓝晶国际约需'+duration2)
            break
            


initial=threading.Thread(target=initial_station)    
initial.start()


timer=threading.Timer(1,locate)
timer.start()
Startime=time.strftime('%H:%M:%S',time.localtime(time.time()))
print('start '+Startime)

#print ('start '+time.strftime('%H:%M:%S',time.localtime(time.time())))

time.sleep(3000)
timer.cancel()
print ('end '+time.strftime('%H:%M:%S',time.localtime(time.time())))
#print(f)
#print("This is console module")
#print(lngx,lngy)


     