#coding:utf-8;
#qpy:2
#qpy:console

#creator:tongy
#collaborators: fengx,cuidongd
#
#Script locates the Android Phone 
#
#
#-------------------------------------
#Imports
import json
import itchat
from androidhelper import Android
import time
from urllib2 import urlopen
import threading
import base64
import random
import busstop
import werobot
#---------------------------------------

#itchat.auto_login(enableCmdQR=True)

#Location in last time
lastloc=0
#i-th station compared
i=0
#The all stations
station=[(30.467499,114.408628),(30.47469,114.409661),(30.489422,114.411117),(30.492301,114.411407),(30.496725,114.416175),(30.494501,114.423904),(30.493554,114.425521)]

def locate():
    #global variables statement
    global station
	global i
	global lastloc
	
	
    d=Android()   
    d.startLocating()
	
    loc=d.getLastKnownLocation().result['gps']
    if loc==None:
        gps=d.getLastKnownLocation().result['network']
    elif loc==lastloc:
        gps=d.getLastKnownLocation().result['network']
    else:
        print('it is gps')
        gps=loc
		
    lngx=gps['longitude']
    lngy=gps['latitude']
 
    lastloc=loc
	
    #Get longitude and latitude in Tencent Map
    ur='http://apis.map.qq.com/ws/coord/v1/translate?locations='+str(lngy)+','+str(lngx)+'&type=1&key=Y5YBZ-VLZCX-EQR4Y-Z47JH-TZCHQ-TXF7H'
    f=urlopen(ur).read()
    f=json.loads(f)
	
    pos_lng=f['locations'][0]['lng']
    pos_lat=f['locations'][0]['lat']
    print(pos_lat)
    print(pos_lng)
	#Latitude and longitude are changed to address
    url='http://apis.map.qq.com/ws/geocoder/v1/?location='+str(pos_lat)+','+str(pos_lng)+'&key=Y5YBZ-VLZCX-EQR4Y-Z47JH-TZCHQ-TXF7H&get_poi=1'
    g=urlopen(url).read()
    g=json.loads(g)
    addr=g[u'result'][u'formatted_addresses'][u'recommend']
    mess=addr.encode('utf-8')
    print(mess)
    
    #werobot.sendmess(addr)
	
	#Judging algorithm
    dis=busstop.distance(pos_lat,pos_lng,station[i][0],station[i][1])
    if dis<=300:
        if i==0:
            print('到达华夏理工')
            time.sleep(random.uniform(0,0.5))
            i=1
            huaxia_duration=busstop.huaxia2optical()
            print('距离光谷天地约需'+huaxia_duration)
                #break
        elif i==1:
            print('光谷天地到了')
            time.sleep(random.uniform(0,0.5))
            i=2
            optical_duration=busstop.optical2xinzhu()
            print('距离新竹路约需'+optical_duration)
                #break
        elif i==2:
            print('抵达新竹路')
            i=3
                #break
        elif i==3:
            print('到达新南路')
            time.sleep(random.uniform(0,0.5))
            i=4
            xinnan_duration=busstop.xinnan2lanjing()
            print('距离蓝晶国际约需'+xinnan_duration)
                #break
        elif i==4:
            print('蓝晶国际到了')
            i=5
                #break
        elif i==5:
            print('到达光谷大道')
            i=6
                #break
        elif i==6:
            print('已到潮漫酒店')
                #break                
    #timer
    global timer
	#Add random constant to control the frequency
    tt=15
    print(tt)
    timer=threading.Timer(tt,locate)
    timer.start()
	
def initial_station():
    while(1):
        currentime=time.strftime('%H:%M:%S',time.localtime(time.time()))
   # print(currentime)
        if currentime=='08:20:00':
            print('发车了')
            [duration1,duration2]=busstop.start2huaxia_lanjing()
            time.sleep(random.uniform(0,0.3))
            print('距离华夏理工约需'+duration1)
            time.sleep(random.uniform(0,0.3))
            print('距离蓝晶国际约需'+duration2)
            break
            
    

initial=threading.Thread(target=initial_station)    
initial.start()
    
timer=threading.Timer(1,locate)
timer.start()
print ('start '+time.strftime('%H:%M:%S',time.localtime(time.time())))
time.sleep(3000)
timer.cancel()
print ('end '+time.strftime('%H:%M:%S',time.localtime(time.time())))



     