#coding:utf-8;
#qpy:2
#qpy:console
import json
import itchat
import re
import time
import threading
import base64
import werobot
import busstop
import datetime
import random
import sys
from androidhelper import Android
from urllib2 import urlopen
from itchat.content import *

reload(sys)
sys.setdefaultencoding("utf-8")
#---------------------------------------------------------------------

class Position:
#---------------------------------------------------------------------
    def __init__(self):
        self.lastloc = ""
		self.loc = ""
        self.lngx = 0 #location from GPS
		self.lngy = 0 
		self.pos_lng = 0 #location from tencent map
		self.pos_lat = 0
		self.i = 0
		self.mess = ""
		self.timer  = ""
        self.station = [(30.467499,114.408628),(30.47469,114.409661),\
                       (30.489422,114.411117),(30.492301,114.411407),\
		               (30.496725,114.416175),(30.494501,114.423904),\
		               (30.493554,114.425521)]
#---------------------------------------------------------------------
#---------------------------------------------------------------------
    def locate(self):
        d = Android()  
        d.startLocating()  
        self.loc = d.getLastKnownLocation().result['gps']
        if self.loc == None:
            gps = d.getLastKnownLocation().result['network']
        elif self.loc == self.lastloc:
            gps = d.getLastKnownLocation().result['network']
        else:
            print('it is gps')
            gps = self.loc
        self.lastloc = self.loc
		
        self.lngx = gps['longitude']
        self.lngy = gps['latitude']
		
		self.translate()
		self.compare_station()
		
        tt=10
        self.timer=threading.Timer(tt,self.locate)
        self.timer.start()

#---------------------------------------------------------------------
#---------------------------------------------------------------------
    def translate(self):   	
        ur = 'http://apis.map.qq.com/ws/coord/v1/translate?locations='\
		    +str(self.lngy)+','+str(self.lngx)+\
			'&type=1&key=Y5YBZ-VLZCX-EQR4Y-Z47JH-TZCHQ-TXF7H'
        f = urlopen(ur).read()
        f = json.loads(f)

        self.pos_lng = f['locations'][0]['lng']
        self.pos_lat = f['locations'][0]['lat']
        print(self.pos_lat)
        print(self.pos_lng)
              
        url = 'http://apis.map.qq.com/ws/geocoder/v1/?location='\
		     +str(self.pos_lat)+','+str(self.pos_lng)+\
			 '&key=Y5YBZ-VLZCX-EQR4Y-Z47JH-TZCHQ-TXF7H&get_poi=1'
        g = urlopen(url).read()
        g = json.loads(g)
        addr = g[u'result'][u'formatted_addresses'][u'recommend']
        self.mess = addr.encode('utf-8')
        print(self.mess)
	
#---------------------------------------------------------------------
#---------------------------------------------------------------------
    def compare_station(self):   
        start = datetime.datetime.now()       
        dis = busstop.distance(self.pos_lat,self.pos_lng,\
		                       self.station[self.i][0],self.station[self.i][1])
        if dis <= 300:
            if self.i == 0:
                werobot.sendmess('到达华夏理工')
                print('到达华夏理工')
                time.sleep(random.uniform(0,0.5))
                self.i = 1
                huaxia_duration = busstop.huaxia2optical()
                werobot.sendmess('距离光谷天地约需'+huaxia_duration)
                print('距离光谷天地约需'+huaxia_duration) 
                #break
            elif self.i == 1:
                werobot.sendmess('光谷天地到了')
                print('光谷天地到了')
                time.sleep(random.uniform(0,0.5))
                self.i = 2
                optical_duration = busstop.optical2xinzhu()
                werobot.sendmess('距离新竹路约需'+optical_duration)
                print('距离新竹路约需'+optical_duration)
                #break
            elif self.i == 2:
                werobot.sendmess('抵达新竹路')
                print('抵达新竹路')
                self.i = 3
                #break
            elif self.i == 3:
                werobot.sendmess('到达新南路')
                print('到达新南路')
                time.sleep(random.uniform(0,0.5))
                self.i = 4
                xinnan_duration = busstop.xinnan2lanjing()
                werobot.sendmess('距离蓝晶国际约需'+xinnan_duration)
                print('距离蓝晶国际约需'+xinnan_duration)
                #break
            elif self.i == 4:
                werobot.sendmess('蓝晶国际到了')
                print('蓝晶国际到了')
                self.i = 5
                #break
            elif self.i == 5:
                werobot.sendmess('到达光谷大道')
                print('到达光谷大道')
                self.i=6
                #break
            elif self.i==6:
                print('已到潮漫酒店')
                #break                
        end=datetime.datetime.now()     
        print (end-start)                
#---------------------------------------------------------------------
#---------------------------------------------------------------------  
    
    def initial_station(self):
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
#---------------------------------------------------------------------           
def main():
    itchat.auto_login(enableCmdQR=True, hotReload=True)
    
	bus_position = Position()
	initial=threading.Thread(target = bus_position.initial_station)    
    initial.start()

    bus_position.timer=threading.Timer(1,bus_position.locate)
    bus_position.timer.start()
    Startime=time.strftime('%H:%M:%S',time.localtime(time.time()))
    print('start '+Startime)

    time.sleep(3000)
    bus_position.timer.cancel()
    print ('end '+time.strftime('%H:%M:%S',time.localtime(time.time())))
#---------------------------------------------------------------------	
if __name__=='__main__':
    main()
#---------------------------------------------------------------------
    


     
