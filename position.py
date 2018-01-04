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
import werobot
#---------------------------------------

#itchat.auto_login(enableCmdQR=True)

def locate():
    d=Android()
    
    d.startLocating()

    loc=d.getLastKnownLocation().result['gps']
    if loc==None:
        gps=d.getLastKnownLocation().result['network']
    else:
        print('it is gps')
        gps=loc
    lngx=gps['longitude']
    lngy=gps['latitude']
 
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

    #timer
    global timer
	#Add random constant to control the frequency
    tt=300+random.uniform(0,30)
    print(tt)
    timer=threading.Timer(tt,locate)
    timer.start()
    
timer=threading.Timer(1,locate)
timer.start()
print ('start '+time.strftime('%H:%M:%S',time.localtime(time.time())))
time.sleep(600)
timer.cancel()
print ('end '+time.strftime('%H:%M:%S',time.localtime(time.time())))



     