#coding:utf-8;
#qpy:2
#qpy:console
import json
import itchat
from androidhelper import Android
import time
#from urllib.request import urlopen
from urllib2 import urlopen
import threading
import base64
import random
import werobot

#itchat.auto_login(enableCmdQR=True)

def locate():
    d=Android()
    
    d.startLocating()
    #time.sleep(3)

    loc=d.getLastKnownLocation().result['gps']
    if loc==None:
        gps=d.getLastKnownLocation().result['network']
    else:
        print('it is gps')
        gps=loc
    #print (loc)
    lngx=gps['longitude']
    lngy=gps['latitude']

#ur='http://api.map.baidu.com/ag/coord/convert?from=0&to=4&x='+str(lngx)+'&y='+str(lngy)
    ur='http://apis.map.qq.com/ws/coord/v1/translate?locations='+str(lngy)+','+str(lngx)+'&type=1&key=Y5YBZ-VLZCX-EQR4Y-Z47JH-TZCHQ-TXF7H'
    f=urlopen(ur).read()
    f=json.loads(f)

#lngx=base64.b64decode(f['x'].encode())
#lngy=base64.b64decode(f['y'].encode())
#lngx=lngx.decode()
#lngy=lngy.decode()

#url='http://lbs.juhe.cn/api/getaddressbylngb?lngx='+str(lngx)+'&lngy'+str(lngy)

#g=urlopen(url).read()
#g=json.loads(g.decode())
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
    
    #werobot.sendmess(addr)

#g=json.loads(g.decode())
 #   print(f['locations'][0]['lat'])
  #  print(f['locations'][0]['lng'])
    global timer
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
#print(f)
#print("This is console module")
#print(lngx,lngy)


     